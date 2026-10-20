from datetime import timedelta
from types import SimpleNamespace
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from .management.commands.seed_logical_exercises import Command
from .models import (
    AccessLevel,
    DailyCycle,
    DailyExerciseProgress,
    Exercise,
    SkillProgress,
    TrainingAttempt,
    TrainingStreak,
    UserTrainingProfile,
)


class TrainingApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='training-user', password='test-password'
        )
        self.other_user = get_user_model().objects.create_user(
            username='other-training-user', password='test-password'
        )
        Command().handle()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def create_profile(self, access_level, expires_at=None):
        return UserTrainingProfile.objects.create(
            user=self.user,
            access_level=access_level,
            access_expires_at=expires_at,
        )

    def test_free_user_gets_three_persisted_random_games_from_first_six(self):
        self.create_profile(AccessLevel.FREE)

        response = self.client.get('/api/training/')

        self.assertEqual(response.status_code, 200)
        cycle = DailyCycle.objects.get(user=self.user)
        selected_numbers = set(cycle.selected_exercises.values_list('number', flat=True))
        self.assertEqual(cycle.daily_limit, 3)
        self.assertEqual(len(selected_numbers), 3)
        self.assertTrue(selected_numbers.issubset(set(range(1, 7))))
        exercise_states = {
            exercise['number']: exercise['state']
            for exercise in response.data['exercises']
        }
        self.assertTrue(all(
            exercise_states[number] == 'CONTENT_PENDING'
            for number in selected_numbers
        ))
        self.assertEqual(exercise_states[10], 'NOT_ACCESSIBLE_BY_LEVEL')

        self.client.get('/api/training/')
        self.assertEqual(
            set(cycle.selected_exercises.values_list('number', flat=True)),
            selected_numbers,
        )

    def test_paid_and_active_temporary_access_get_all_ten_games(self):
        for level in (AccessLevel.PLUS, AccessLevel.PRO):
            with self.subTest(level=level):
                user = get_user_model().objects.create_user(username=level.lower())
                UserTrainingProfile.objects.create(user=user, access_level=level)
                client = APIClient()
                client.force_authenticate(user)

                response = client.get('/api/training/')

                self.assertEqual(response.data['daily_limit'], 10)
                self.assertEqual(len(response.data['exercises']), 10)
                self.assertTrue(all(
                    exercise['state'] == 'CONTENT_PENDING'
                    for exercise in response.data['exercises']
                ))

        self.create_profile(
            AccessLevel.ALUMNO_PLUS_TEMPORAL,
            timezone.now() + timedelta(days=1),
        )
        response = self.client.get('/api/training/')
        self.assertEqual(response.data['daily_limit'], 10)

    def test_expired_temporary_access_falls_back_to_free(self):
        self.create_profile(
            AccessLevel.ALUMNO_PLUS_TEMPORAL,
            timezone.now() - timedelta(seconds=1),
        )

        response = self.client.get('/api/training/')

        self.assertEqual(response.data['access_level'], AccessLevel.FREE)
        self.assertEqual(response.data['daily_limit'], 3)

    def test_cycle_downgrades_when_temporary_access_expires(self):
        profile = self.create_profile(
            AccessLevel.ALUMNO_PLUS_TEMPORAL,
            timezone.now() + timedelta(days=1),
        )
        self.client.get('/api/training/')
        cycle = DailyCycle.objects.get(user=self.user)
        self.assertEqual(cycle.selected_exercises.count(), 10)

        profile.access_expires_at = timezone.now() - timedelta(seconds=1)
        profile.save(update_fields=['access_expires_at'])
        response = self.client.get('/api/training/')

        cycle.refresh_from_db()
        self.assertEqual(response.data['access_level'], AccessLevel.FREE)
        self.assertEqual(cycle.daily_limit, 3)
        selected_numbers = set(cycle.selected_exercises.values_list('number', flat=True))
        self.assertEqual(len(selected_numbers), 3)
        self.assertTrue(selected_numbers.issubset(set(range(1, 7))))

    def test_successful_completion_updates_skill_once_and_does_not_grant_xp(self):
        self.create_profile(AccessLevel.PLUS)
        assignment = SimpleNamespace(variant_key='test-variant')
        variant = {
            'expected_order': ['first', 'second'],
            'explanation': 'Orden incorrecto.',
        }
        with patch(
            'apps.training.views.catalog.get_or_assign_monthly_variant',
            return_value=(assignment, variant),
        ):
            first = self.client.post(
                '/api/training/exercises/1/submit/',
                {'answer': {'ordered_ids': ['first', 'second']}},
                format='json',
            )
            second = self.client.post(
                '/api/training/exercises/1/submit/',
                {'answer': {'ordered_ids': ['first', 'second']}},
                format='json',
            )

        self.assertTrue(first.data['correct'])
        self.assertEqual(first.data['xp_per_completed_game'], 5)
        self.assertFalse(first.data['xp_granted'])
        self.assertFalse(first.data['ducky_coins_granted'])
        self.assertEqual(second.data['attempt_number'], 2)
        self.assertEqual(
            SkillProgress.objects.get(user=self.user, skill='Secuenciación').successful_completions,
            1,
        )
        progress = DailyExerciseProgress.objects.get(
            cycle__user=self.user, exercise__number=1
        )
        self.assertFalse(progress.xp_reward_processed)
        self.assertFalse(progress.ducky_coin_reward_processed)

    def test_attempt_limit_is_five_per_user_game_and_cycle(self):
        self.create_profile(AccessLevel.PLUS)
        with patch(
            'apps.training.views.catalog.get_or_assign_monthly_variant',
            return_value=(
                SimpleNamespace(variant_key='test-variant'),
                {'expected_order': ['right'], 'explanation': 'Orden incorrecto.'},
            ),
        ):
            for expected_attempt in range(1, 6):
                response = self.client.post(
                    '/api/training/exercises/1/submit/',
                    {'answer': {'ordered_ids': ['wrong']}},
                    format='json',
                )
                self.assertEqual(response.data['attempt_number'], expected_attempt)

            sixth = self.client.post(
                '/api/training/exercises/1/submit/',
                {'answer': {'ordered_ids': ['wrong']}},
                format='json',
            )

        self.assertEqual(sixth.status_code, 409)
        self.assertEqual(TrainingAttempt.objects.filter(user=self.user).count(), 5)

    def test_unpublished_content_does_not_create_a_fake_attempt(self):
        self.create_profile(AccessLevel.PLUS)
        with patch(
            'apps.training.views.catalog.get_or_assign_monthly_variant',
            return_value=(None, None),
        ):
            response = self.client.post(
                '/api/training/exercises/1/submit/',
                {'answer': {'ordered_ids': ['anything']}},
                format='json',
            )

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.data['error'], 'educational_content_pending')
        self.assertEqual(TrainingAttempt.objects.filter(user=self.user).count(), 0)

    def test_history_and_progress_only_return_authenticated_users_data(self):
        self.create_profile(AccessLevel.PLUS)
        cycle = DailyCycle.objects.create(
            user=self.user,
            cycle_date=timezone.localdate(),
            effective_access_level=AccessLevel.PLUS,
            daily_limit=10,
        )
        exercise = Exercise.objects.get(number=1)
        TrainingAttempt.objects.create(
            user=self.user,
            exercise=exercise,
            cycle=cycle,
            answer_payload={'ordered_ids': []},
            is_correct=False,
            variant_reference='variant',
            attempt_number=1,
        )
        other_cycle = DailyCycle.objects.create(
            user=self.other_user,
            cycle_date=timezone.localdate(),
            effective_access_level=AccessLevel.FREE,
            daily_limit=3,
        )
        TrainingAttempt.objects.create(
            user=self.other_user,
            exercise=exercise,
            cycle=other_cycle,
            answer_payload={'ordered_ids': []},
            is_correct=True,
            variant_reference='other-variant',
            attempt_number=1,
        )
        SkillProgress.objects.create(
            user=self.other_user,
            skill='Other user skill',
            successful_completions=4,
        )

        history = self.client.get('/api/training/history/?limit=20')
        progress = self.client.get('/api/training/progress/')

        self.assertEqual(len(history.data['results']), 1)
        self.assertEqual(history.data['results'][0]['attempt_number'], 1)
        self.assertEqual(progress.data['skills'], [])
        self.assertEqual(progress.data['streak']['current'], 0)

    def test_history_rejects_invalid_limit(self):
        response = self.client.get('/api/training/history/?limit=101')
        self.assertEqual(response.status_code, 400)

    def test_streak_advances_when_daily_selection_is_completed_once(self):
        self.create_profile(AccessLevel.FREE)
        cycle = DailyCycle.objects.create(
            user=self.user,
            cycle_date=timezone.localdate(),
            effective_access_level=AccessLevel.FREE,
            daily_limit=3,
        )
        selected = list(Exercise.objects.filter(number__in=[1, 2, 3]))
        cycle.selected_exercises.set(selected)
        for exercise in selected[:2]:
            DailyExerciseProgress.objects.create(
                cycle=cycle, exercise=exercise, completed=True
            )

        with patch(
            'apps.training.views.catalog.get_or_assign_monthly_variant',
            return_value=(
                SimpleNamespace(variant_key='test-variant'),
                {'expected_bug_id': 'bug', 'explanation': 'Error incorrecto.'},
            ),
        ):
            response = self.client.post(
                '/api/training/exercises/3/submit/',
                {'answer': {'selected_bug_id': 'bug'}},
                format='json',
            )

        self.assertTrue(response.data['correct'])
        streak = TrainingStreak.objects.get(user=self.user)
        self.assertEqual(streak.current_streak, 1)
        cycle.refresh_from_db()
        self.assertTrue(cycle.streak_processed)
