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
    MonthlyVariantAssignment,
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
                    and exercise['content_status'] is None
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
            'content_status': 'published',
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
                {
                    'expected_order': ['right'],
                    'explanation': 'Orden incorrecto.',
                    'content_status': 'published',
                },
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
                {
                    'expected_bug_id': 'bug',
                    'explanation': 'Error incorrecto.',
                    'content_status': 'published',
                },
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
    def test_catalog_has_one_explicit_provisional_variant_for_each_game(self):
        from .catalog import get_catalog, clear_catalog_cache, validate_variant_content

        clear_catalog_cache()
        catalog = get_catalog()
        self.assertEqual([item['exercise_number'] for item in catalog['exercises']], list(range(1, 11)))
        for item in catalog['exercises']:
            self.assertEqual(len(item['variants']), 1)
            variant = item['variants'][0]
            self.assertEqual(variant['status'], 'provisional')
            self.assertTrue(variant['variant_key'])
            self.assertIn('CONTENIDO EDUCATIVO PROVISIONAL', variant['content']['provisional_notice'])
            validate_variant_content(item['exercise_type'], variant['content'])

    def test_provisional_variant_cannot_be_submitted_or_completed(self):
        from .catalog import get_variant

        self.create_profile(AccessLevel.PLUS)
        self.assertIsNone(get_variant(
            'ex01_temp_v1',
            expected_exercise_number=1,
            expected_type='ORDER_ALGORITHM',
        ))

        response = self.client.post(
            '/api/training/exercises/1/submit/',
            {'answer': {'ordered_ids': ['start', 'check', 'finish']}},
            format='json',
        )

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.data['error'], 'educational_content_pending')
        self.assertEqual(TrainingAttempt.objects.filter(user=self.user).count(), 0)
        progress = DailyExerciseProgress.objects.get(
            cycle__user=self.user, exercise__number=1
        )
        self.assertFalse(progress.completed)

    def test_removed_variant_assignment_is_pending_without_reassignment(self):
        self.create_profile(AccessLevel.PLUS)
        exercise = Exercise.objects.get(number=3)
        assignment = MonthlyVariantAssignment.objects.create(
            user=self.user,
            exercise=exercise,
            month=timezone.localdate().replace(day=1),
            variant_key='ex03_v1',
        )

        overview = self.client.get('/api/training/')
        exercise_data = next(
            item for item in overview.data['exercises'] if item['number'] == 3
        )
        self.assertEqual(overview.status_code, 200)
        self.assertEqual(exercise_data['state'], 'CONTENT_PENDING')
        self.assertIsNone(exercise_data['content'])

        response = self.client.post(
            '/api/training/exercises/3/submit/',
            {'answer': {'selected_bug_id': 'bug'}},
            format='json',
        )

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.data['error'], 'educational_content_pending')
        self.assertEqual(TrainingAttempt.objects.filter(user=self.user).count(), 0)
        assignment.refresh_from_db()
        self.assertEqual(assignment.variant_key, 'ex03_v1')
        progress = DailyExerciseProgress.objects.get(
            cycle__user=self.user, exercise=exercise
        )
        self.assertFalse(progress.completed)

    def test_associate_concepts_type_is_not_supported_by_catalog_validator(self):
        from .catalog import CatalogError, validate_variant_content

        content = {
            'instruction': 'Relaciona conceptos.',
            'explanation': 'Explicación.',
            'prompt': 'Asocia.',
            'content_version': 'source-v1',
            'validation_rules': 'Pending contract.',
            'error_explanation': 'Respuesta incorrecta.',
            'provisional_notice': 'CONTENIDO EDUCATIVO PROVISIONAL',
            'input_data': {},
        }

        with self.assertRaises(CatalogError):
            validate_variant_content('asociar_conceptos', content)

    def test_provided_practice_games_hide_solutions_until_submission(self):
        response = self.client.get('/api/training/provided-games/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            {game['id'] for game in response.data['games']},
            {'asociar_conceptos', 'detectar_error', 'ordenar_codigo'},
        )
        self.assertTrue(all(
            game['content_status'] == 'provisional'
            for game in response.data['games']
        ))

        paths = {
            'asociar_conceptos': ('asociaciones',),
            'detectar_error': ('error',),
            'ordenar_codigo': ('orden_correcto',),
        }
        for game_id, forbidden_fields in paths.items():
            with self.subTest(game_id=game_id):
                challenge = self.client.get(
                    f'/api/training/provided-games/{game_id}/1/'
                )
                self.assertEqual(challenge.status_code, 200)
                self.assertEqual(challenge.data['game']['content_status'], 'provisional')
                self.assertTrue(all(
                    field not in challenge.data['content']
                    for field in forbidden_fields
                ))

    def test_provided_practice_answers_are_server_validated_without_daily_progress(self):
        from .provided_games import _load_game

        def association_answer(exercise):
            concepts = {item['id']: item['texto'] for item in exercise['conceptos']}
            explanations = {item['id']: item['texto'] for item in exercise['explicaciones']}
            return {
                'asociaciones': [
                    {
                        'concepto': concepts[pair['concepto_id']],
                        'explicacion': explanations[pair['explicacion_id']],
                    }
                    for pair in exercise['asociaciones']
                ],
            }

        cases = {
            'asociar_conceptos': association_answer,
            'detectar_error': lambda exercise: {
                'selected_line': next(line['linea'] for line in exercise['codigo'] if line['error'] is True),
            },
            'ordenar_codigo': lambda exercise: {
                'ordered_ids': exercise['orden_correcto'],
            },
        }
        for game_id, make_answer in cases.items():
            with self.subTest(game_id=game_id):
                challenge = self.client.get(
                    f'/api/training/provided-games/{game_id}/1/'
                )
                source = _load_game(game_id)
                exercise = next(
                    item
                    for level in source['niveles']
                    for item in level['pruebas']
                    if item['id'] == challenge.data['exercise_id']
                )
                response = self.client.post(
                    f'/api/training/provided-games/{game_id}/1/',
                    {
                        'exercise_id': challenge.data['exercise_id'],
                        'answer': make_answer(exercise),
                    },
                    format='json',
                )

                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.data['correct'])
                self.assertNotIn('xp_granted', response.data)
                self.assertFalse(TrainingAttempt.objects.filter(user=self.user).exists())
                self.assertFalse(DailyExerciseProgress.objects.filter(
                    cycle__user=self.user, completed=True
                ).exists())

    def test_existing_provisional_completion_is_not_counted_in_daily_progress(self):
        self.create_profile(AccessLevel.PLUS)
        self.client.get('/api/training/')
        cycle = DailyCycle.objects.get(user=self.user)
        exercise = Exercise.objects.get(number=1)
        DailyExerciseProgress.objects.create(
            cycle=cycle, exercise=exercise, completed=True
        )
        MonthlyVariantAssignment.objects.create(
            user=self.user,
            exercise=exercise,
            month=timezone.localdate().replace(day=1),
            variant_key='ex01_temp_v1',
        )

        response = self.client.get('/api/training/')

        self.assertEqual(response.data['completed_count'], 0)
        exercise_state = next(
            item for item in response.data['exercises'] if item['number'] == 1
        )
        self.assertEqual(exercise_state['state'], 'CONTENT_PENDING')

    def test_empty_expected_answer_cannot_be_correct(self):
        from .validators import validate_sorting, validate_networking, validate_bug_finding

        self.assertFalse(validate_sorting({'expected_order': [], 'explanation': 'x'}, {'ordered_ids': []})[0])
        self.assertFalse(validate_networking({'expected_connections': [], 'explanation': 'x'}, {'connections': []})[0])
        self.assertFalse(validate_bug_finding({'expected_bug_id': '', 'explanation': 'x'}, {'selected_bug_id': ''})[0])
