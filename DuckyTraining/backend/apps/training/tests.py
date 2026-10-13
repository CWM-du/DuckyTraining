from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch
from datetime import timedelta , date


from .management.commands.seed_logical_exercises import Command
from .models import (
    AccessLevel, DailyCycle, DailyExerciseProgress, Exercise,
    MonthlyVariantAssignment, SkillProgress, TrainingAttempt, TrainingStreak, UserTrainingProfile
)

class TrainingOverviewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test-user', password='test-pass')
        Command().handle()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_free_gets_three_random_games_from_one_to_six_and_selection_persists(self):
        first = self.client.get('/api/training/')
        self.assertEqual(first.status_code, 200)
        self.assertEqual(first.data['daily_limit'], 3)
        selected = first.data['selected_exercise_numbers']
        self.assertEqual(len(selected), 3)
        self.assertEqual(len(set(selected)), 3)
        self.assertTrue(set(selected).issubset({1, 2, 3, 4, 5, 6}))

        by_number = {exercise['number']: exercise for exercise in first.data['exercises']}
        for number in selected:
            self.assertEqual(by_number[number]['state'], 'AVAILABLE')
        for number in (7, 8, 9, 10):
            self.assertEqual(by_number[number]['state'], 'NOT_ACCESSIBLE_BY_LEVEL')

        second = self.client.get('/api/training/')
        self.assertEqual(second.data['selected_exercise_numbers'], selected)

    def test_free_selected_games_have_no_sequential_block(self):
        response = self.client.get('/api/training/')
        selected = response.data['selected_exercise_numbers']
        self.assertEqual(len(selected), 3)
        states = {item['number']: item['state'] for item in response.data['exercises']}
        self.assertTrue(all(states[number] == 'AVAILABLE' for number in selected))
        self.assertNotIn('BLOCKED_BY_SEQUENCE', states.values())

    def test_plus_and_pro_can_access_all_ten_without_sequence(self):
        for level in (AccessLevel.PLUS, AccessLevel.PRO):
            user = get_user_model().objects.create_user(username=f'{level.lower()}-user', password='test-pass')
            UserTrainingProfile.objects.create(user=user, access_level=level)
            client = APIClient()
            client.force_authenticate(user)
            response = client.get('/api/training/')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data['daily_limit'], 10)
            self.assertEqual(len(response.data['exercises']), 10)
            self.assertTrue(all(item['state'] == 'AVAILABLE' for item in response.data['exercises']))

    def test_temporary_plus_keeps_legacy_sequential_behavior(self):
        UserTrainingProfile.objects.create(user=self.user, access_level=AccessLevel.ALUMNO_PLUS_TEMPORAL)
        response = self.client.get('/api/training/')
        states = {item['number']: item['state'] for item in response.data['exercises']}
        self.assertEqual(response.data['daily_limit'], 5)
        self.assertEqual(states[1], 'AVAILABLE')
        self.assertEqual(states[2], 'BLOCKED_BY_SEQUENCE')
        self.assertEqual(states[6], 'NOT_ACCESSIBLE_BY_LEVEL')

    def test_daily_cycle_uses_madrid_timezone_setting(self):
        from django.conf import settings
        self.assertEqual(settings.TIME_ZONE, 'Europe/Madrid')

class ExerciseSubmitViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test-submitter', password='password123')
        
        # Poblamos la BD con los ejercicios predefinidos
        Command().handle()
        
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        UserTrainingProfile.objects.create(
            user=self.user,
            access_level=AccessLevel.FREE
        )
        
        # Fija una selección de prueba estable para que los tests del endpoint no dependan del azar.
        self.cycle = DailyCycle.objects.create(
            user=self.user,
            cycle_date=timezone.localdate(),
            effective_access_level=AccessLevel.FREE,
            daily_limit=3,
        )
        self.cycle.selected_exercises.set(Exercise.objects.filter(number__in=[1, 2, 3]))

        # Recuperamos el ejercicio 1 creado por el seeder
        self.exercise = Exercise.objects.get(number=1)
        
        today = timezone.localdate()
        first_day_of_month = today.replace(day=1)
        MonthlyVariantAssignment.objects.create(
            user=self.user,
            exercise=self.exercise,
            month=first_day_of_month,
            variant_key="ex01_v1"
        )
        
        self.url = f'/api/training/exercises/{self.exercise.number}/submit/'

    @patch('apps.training.views.get_or_assign_monthly_variant')
    def test_first_attempt_registers_correctly(self, mock_variant):
        assignment = MonthlyVariantAssignment.objects.get(user=self.user, exercise=self.exercise)
        variant = {
            'variant_key': 'ex01_v1', 'exercise_number': 1, 'exercise_type': 'ORDER_ALGORITHM',
            'instruction': 'Ordena los pasos.', 'steps': [{'id': 'a', 'text': 'Paso A'}, {'id': 'b', 'text': 'Paso B'}],
            'expected_order': ['a', 'b'], 'explanation': 'Revisa el orden lógico.'
        }
        mock_variant.return_value = (assignment, variant)
        payload = {"answer": {"ordered_ids": ["a", "b"]}}
        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertTrue(response.data['correct'])
        self.assertEqual(response.data['attempt_number'], 1)
        self.assertEqual(TrainingAttempt.objects.count(), 1)
        skill_progress = SkillProgress.objects.get(user=self.user, skill=self.exercise.skill)
        self.assertEqual(skill_progress.successful_completions, 1)

    @patch('apps.training.views.get_or_assign_monthly_variant')
    def test_repeated_correct_attempt_is_history_but_not_extra_skill_completion(self, mock_variant):
        assignment = MonthlyVariantAssignment.objects.get(user=self.user, exercise=self.exercise)
        variant = {
            'variant_key': 'ex01_v1', 'exercise_number': 1, 'exercise_type': 'ORDER_ALGORITHM',
            'instruction': 'Ordena los pasos.', 'steps': [{'id': 'a', 'text': 'Paso A'}, {'id': 'b', 'text': 'Paso B'}],
            'expected_order': ['a', 'b'], 'explanation': 'Revisa el orden lógico.'
        }
        mock_variant.return_value = (assignment, variant)
        payload = {'answer': {'ordered_ids': ['a', 'b']}}

        first = self.client.post(self.url, payload, format='json')
        second = self.client.post(self.url, payload, format='json')

        self.assertEqual(first.status_code, status.HTTP_200_OK)
        self.assertEqual(second.status_code, status.HTTP_200_OK)
        self.assertEqual(TrainingAttempt.objects.filter(user=self.user, exercise=self.exercise).count(), 2)
        skill_progress = SkillProgress.objects.get(user=self.user, skill=self.exercise.skill)
        self.assertEqual(skill_progress.successful_completions, 1)
        self.cycle.refresh_from_db()
        self.assertEqual(self.cycle.completed_count, 1)

    @patch('apps.training.views.get_or_assign_monthly_variant')
    def test_five_attempt_limit_is_enforced(self, mock_variant):
        assignment = MonthlyVariantAssignment.objects.get(user=self.user, exercise=self.exercise)
        variant = {
            'variant_key': 'ex01_v1', 'exercise_number': 1, 'exercise_type': 'ORDER_ALGORITHM',
            'instruction': 'Ordena los pasos.', 'steps': [{'id': 'a', 'text': 'Paso A'}, {'id': 'b', 'text': 'Paso B'}],
            'expected_order': ['a', 'b'], 'explanation': 'Revisa el orden lógico.'
        }
        mock_variant.return_value = (assignment, variant)
        payload = {"answer": {"ordered_ids": ["mal"]}}

        for i in range(5):
            response = self.client.post(self.url, payload, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['attempt_number'], i + 1)

        response_6 = self.client.post(self.url, payload, format='json')
        self.assertEqual(response_6.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response_6.data['error'], 'attempt_limit_reached')
        self.assertEqual(TrainingAttempt.objects.count(), 5)

    def test_variant_pending_content_returns_service_unavailable(self):
        exercise2 = Exercise.objects.get(number=2)
        cycle = self.cycle
        DailyExerciseProgress.objects.create(cycle=cycle, exercise=self.exercise, completed=True)
        MonthlyVariantAssignment.objects.create(
            user=self.user, exercise=exercise2, month=timezone.localdate().replace(day=1), variant_key='ex02_v1'
        )
        response = self.client.post(
            f'/api/training/exercises/{exercise2.number}/submit/',
            {"answer": {"ordered_ids": ["step_1"]}}, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertEqual(response.data['error'], 'variant_content_pending')
        self.assertEqual(TrainingAttempt.objects.count(), 0)

    def test_unknown_variant_key_is_configuration_error(self):
        MonthlyVariantAssignment.objects.filter(user=self.user, exercise=self.exercise).update(variant_key='unknown_key')
        response = self.client.post(self.url, {"answer": {"ordered_ids": ["x"]}}, format='json')
        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertEqual(response.data['error'], 'catalog_configuration_error')
        self.assertEqual(TrainingAttempt.objects.count(), 0)


from unittest.mock import patch
from datetime import timedelta, date

class DailyCycleAdvancedTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='pro-user', password='password123')
        Command().handle()
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        UserTrainingProfile.objects.create(user=self.user, access_level=AccessLevel.PRO)

    def test_pro_user_gets_all_ten_games_without_sequence(self):
        response = self.client.get('/api/training/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['daily_limit'], 10)
        self.assertEqual(len(response.data['exercises']), 10)
        self.assertTrue(all(item['state'] == 'AVAILABLE' for item in response.data['exercises']))

    @patch('apps.training.views.timezone.localdate')
    def test_daily_reset_and_history_retention(self, mock_localdate):
        base_date = date(2026, 10, 13)
        mock_localdate.return_value = base_date
        response_day1 = self.client.get('/api/training/')
        cycle_day1 = DailyCycle.objects.get(user=self.user, cycle_date=base_date)
        exercise_one = Exercise.objects.get(number=1)
        DailyExerciseProgress.objects.create(cycle=cycle_day1, exercise=exercise_one, completed=True)

        response_day1_after = self.client.get('/api/training/')
        self.assertEqual(response_day1_after.data['exercises'][0]['state'], 'COMPLETED_TODAY')
        self.assertEqual(response_day1_after.data['exercises'][1]['state'], 'AVAILABLE')

        next_day = base_date + timedelta(days=1)
        mock_localdate.return_value = next_day
        response_day2 = self.client.get('/api/training/')
        self.assertEqual(response_day2.data['daily_limit'], 10)
        self.assertEqual(response_day2.data['exercises'][0]['state'], 'AVAILABLE')
        self.assertEqual(response_day2.data['exercises'][1]['state'], 'AVAILABLE')

        self.assertEqual(DailyCycle.objects.count(), 2)
        self.assertTrue(DailyCycle.objects.filter(user=self.user, cycle_date=base_date).exists())
        self.assertTrue(DailyCycle.objects.filter(user=self.user, cycle_date=next_day).exists())

    def test_plus_user_has_full_catalog(self):
        plus_user = get_user_model().objects.create_user(username='plus-user', password='password123')
        UserTrainingProfile.objects.create(user=plus_user, access_level=AccessLevel.PLUS)
        client = APIClient()
        client.force_authenticate(plus_user)
        response = client.get('/api/training/')
        self.assertEqual(response.data['daily_limit'], 10)
        self.assertTrue(all(item['state'] == 'AVAILABLE' for item in response.data['exercises']))

class EducationalCatalogStructureTests(TestCase):
    def test_catalog_has_five_pending_slots_for_each_of_ten_games(self):
        from .catalog import get_catalog
        catalog = get_catalog()
        self.assertEqual(len(catalog['exercises']), 10)
        for entry in catalog['exercises']:
            self.assertEqual(len(entry['variants']), 5)
            self.assertTrue(all(item['status'] == 'pending_content' and item['content'] is None for item in entry['variants']))

    def test_game_ten_is_find_error_in_seed_definition(self):
        Command().handle()
        game_ten = Exercise.objects.get(number=10)
        self.assertEqual(game_ten.exercise_type, 'FIND_ERROR')

    def test_empty_answer_cannot_pass_empty_solution(self):
        from .validators import validate_sorting
        correct, _ = validate_sorting({'expected_order': [], 'explanation': 'Explicación'}, {'ordered_ids': []})
        self.assertFalse(correct)


class TrainingProgressAndHistoryTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='f7-user', password='password123')
        self.other_user = get_user_model().objects.create_user(username='f7-other', password='password123')
        Command().handle()
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.exercise = Exercise.objects.get(number=1)
        self.today = timezone.localdate()
        self.cycle = DailyCycle.objects.create(
            user=self.user, cycle_date=self.today, effective_access_level=AccessLevel.FREE, daily_limit=3
        )
        self.cycle.selected_exercises.set(Exercise.objects.filter(number__in=[1, 2, 3]))

    def test_progress_endpoint_returns_only_user_skill_data_and_quota(self):
        SkillProgress.objects.create(user=self.user, skill='Algoritmos', successful_completions=2)
        SkillProgress.objects.create(user=self.other_user, skill='Redes', successful_completions=99)
        response = self.client.get('/api/training/progress/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['daily_quota'], 3)
        self.assertEqual(response.data['completed_count'], 0)
        self.assertEqual(response.data['skills'], [{'skill': 'Algoritmos', 'successful_completions': 2}])
        self.assertEqual(response.data['streak']['current_streak'], 0)

    def test_history_endpoint_returns_only_authenticated_users_attempts(self):
        TrainingAttempt.objects.create(
            user=self.user, exercise=self.exercise, cycle=self.cycle, answer_payload={'ordered_ids': ['a']},
            is_correct=False, error_explanation='Prueba', variant_reference='ex01_v1', attempt_number=1
        )
        other_cycle = DailyCycle.objects.create(
            user=self.other_user, cycle_date=self.today, effective_access_level=AccessLevel.FREE, daily_limit=3
        )
        TrainingAttempt.objects.create(
            user=self.other_user, exercise=self.exercise, cycle=other_cycle, answer_payload={'ordered_ids': ['b']},
            is_correct=True, error_explanation='', variant_reference='ex01_v1', attempt_number=1
        )
        response = self.client.get('/api/training/history/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['exercise_number'], 1)
        self.assertFalse(response.data['results'][0]['is_correct'])

    def test_history_limit_is_validated(self):
        response = self.client.get('/api/training/history/?limit=101')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_streak_only_updates_when_daily_quota_is_complete(self):
        from apps.training.views import update_streak_if_quota_complete
        DailyExerciseProgress.objects.create(cycle=self.cycle, exercise=Exercise.objects.get(number=1), completed=True)
        self.assertFalse(update_streak_if_quota_complete(self.cycle, self.today))
        self.assertFalse(TrainingStreak.objects.filter(user=self.user).exists())

        for number in (2, 3):
            DailyExerciseProgress.objects.create(
                cycle=self.cycle, exercise=Exercise.objects.get(number=number), completed=True
            )
        self.assertTrue(update_streak_if_quota_complete(self.cycle, self.today))
        streak = TrainingStreak.objects.get(user=self.user)
        self.assertEqual(streak.current_streak, 1)
        self.assertEqual(streak.last_completion_date, self.today)
        self.cycle.refresh_from_db()
        self.assertTrue(self.cycle.streak_processed)
        self.assertFalse(update_streak_if_quota_complete(self.cycle, self.today))
        self.assertEqual(TrainingStreak.objects.get(user=self.user).current_streak, 1)

    def test_streak_increments_only_for_consecutive_completed_days(self):
        from apps.training.views import update_streak_if_quota_complete
        yesterday = self.today - timedelta(days=1)
        TrainingStreak.objects.create(user=self.user, current_streak=3, last_completion_date=yesterday)
        for number in (1, 2, 3):
            DailyExerciseProgress.objects.create(
                cycle=self.cycle, exercise=Exercise.objects.get(number=number), completed=True
            )
        self.assertTrue(update_streak_if_quota_complete(self.cycle, self.today))
        streak = TrainingStreak.objects.get(user=self.user)
        self.assertEqual(streak.current_streak, 4)
        self.assertEqual(streak.last_completion_date, self.today)
