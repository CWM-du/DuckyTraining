from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from .management.commands.seed_logical_exercises import Command
from .models import (
    AccessLevel, DailyCycle, DailyExerciseProgress, Exercise,
    MonthlyVariantAssignment, TrainingAttempt, UserTrainingProfile
)

class TrainingOverviewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test-user', password='test-pass')
        Command().handle()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_free_user_gets_three_daily_exercises(self):
        # Cambiado a la ruta correcta sin el "overview/"
        response = self.client.get('/api/training/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['daily_limit'], 3)
        self.assertEqual(response.data['exercises'][0]['state'], 'AVAILABLE')
        self.assertEqual(response.data['exercises'][1]['state'], 'BLOCKED_BY_SEQUENCE')
        self.assertEqual(response.data['exercises'][3]['state'], 'NOT_ACCESSIBLE_BY_LEVEL')

    def test_completed_previous_exercise_unlocks_next(self):
        # Cambiado a la ruta correcta
        response = self.client.get('/api/training/')
        cycle = DailyCycle.objects.get(user=self.user)
        exercise_one = Exercise.objects.get(number=1)
        DailyExerciseProgress.objects.create(cycle=cycle, exercise=exercise_one, completed=True)
        
        # Cambiado a la ruta correcta
        response = self.client.get('/api/training/')
        self.assertEqual(response.data['exercises'][1]['state'], 'AVAILABLE')

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
        
        # Recuperamos el ejercicio 1 creado por el seeder
        self.exercise = Exercise.objects.get(number=1)
        
        today = timezone.localdate()
        first_day_of_month = today.replace(day=1)
        MonthlyVariantAssignment.objects.create(
            user=self.user,
            exercise=self.exercise,
            month=first_day_of_month,
            variant_key="var_123"
        )
        
        self.url = f'/api/training/exercises/{self.exercise.number}/submit/'

    def test_first_attempt_registers_correctly(self):
        payload = {"answer": {"ordered_ids": []}}
        response = self.client.post(self.url, payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['attempt_number'], 1)
        self.assertEqual(TrainingAttempt.objects.count(), 1)

    def test_five_attempt_limit_is_enforced(self):
        payload = {"answer": {"ordered_ids": ["mal"]}}
        
        for i in range(5):
            response = self.client.post(self.url, payload, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['attempt_number'], i + 1)
            
        response_6 = self.client.post(self.url, payload, format='json')
        self.assertEqual(response_6.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response_6.data['error'], 'attempt_limit_reached')
        self.assertEqual(TrainingAttempt.objects.count(), 5)

    def test_variant_not_found_returns_404(self):
        # Recuperamos el ejercicio 2 que no tiene variante asignada en setUp
        exercise2 = Exercise.objects.get(number=2)
        
        # Simulamos que completó el ejercicio 1 para que el sistema le deje acceder al 2
        cycle = DailyCycle.objects.create(user=self.user, cycle_date=timezone.localdate(), effective_access_level=AccessLevel.FREE, daily_limit=3)
        DailyExerciseProgress.objects.create(cycle=cycle, exercise=self.exercise, completed=True)

        url2 = f'/api/training/exercises/{exercise2.number}/submit/'
        payload = {"answer": {"selected_bug_id": "line_1"}}
        
        response = self.client.post(url2, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'variant_not_found')