from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from .management.commands.seed_logical_exercises import Command
from .models import AccessLevel, DailyCycle, DailyExerciseProgress, Exercise


class TrainingOverviewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test-user', password='test-pass')
        Command().handle()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_free_user_gets_three_daily_exercises(self):
        response = self.client.get('/api/training/overview/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['daily_limit'], 3)
        self.assertEqual(response.data['exercises'][0]['state'], 'AVAILABLE')
        self.assertEqual(response.data['exercises'][1]['state'], 'BLOCKED_BY_SEQUENCE')
        self.assertEqual(response.data['exercises'][3]['state'], 'NOT_ACCESSIBLE_BY_LEVEL')

    def test_completed_previous_exercise_unlocks_next(self):
        response = self.client.get('/api/training/overview/')
        cycle = DailyCycle.objects.get(user=self.user)
        exercise_one = Exercise.objects.get(number=1)
        DailyExerciseProgress.objects.create(cycle=cycle, exercise=exercise_one, completed=True)
        response = self.client.get('/api/training/overview/')
        self.assertEqual(response.data['exercises'][1]['state'], 'AVAILABLE')
