from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    AccessLevel, DAILY_LIMITS, DailyCycle, DailyExerciseProgress, Exercise,
    TrainingAttempt, UserTrainingProfile,
)


def get_or_create_daily_cycle(user, cycle_date):
    profile, _ = UserTrainingProfile.objects.get_or_create(user=user)
    cycle, _ = DailyCycle.objects.get_or_create(
        user=user,
        cycle_date=cycle_date,
        defaults={
            'effective_access_level': profile.access_level,
            'daily_limit': DAILY_LIMITS[profile.access_level],
        },
    )
    return cycle


def exercise_state(cycle, exercise):
    progress = DailyExerciseProgress.objects.filter(cycle=cycle, exercise=exercise).first()
    if progress and progress.completed:
        return 'COMPLETED_TODAY'
    if exercise.number > cycle.daily_limit:
        return 'NOT_ACCESSIBLE_BY_LEVEL'
    if exercise.number == 1:
        return 'AVAILABLE'
    previous_completed = DailyExerciseProgress.objects.filter(
        cycle=cycle, exercise__number=exercise.number - 1, completed=True
    ).exists()
    return 'AVAILABLE' if previous_completed else 'BLOCKED_BY_SEQUENCE'


class TrainingOverviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cycle_date = timezone.localdate()
        cycle = get_or_create_daily_cycle(request.user, cycle_date)
        exercises = []
        for exercise in Exercise.objects.filter(active=True):
            exercises.append({
                'number': exercise.number,
                'name': exercise.logical_name,
                'type': exercise.exercise_type,
                'difficulty': exercise.difficulty,
                'skill': exercise.skill,
                'state': exercise_state(cycle, exercise),
            })
        return Response({
            'access_level': cycle.effective_access_level,
            'daily_limit': cycle.daily_limit,
            'cycle_date': cycle_date,
            'completed_count': cycle.completed_count,
            'exercises': exercises,
        })


class ExerciseSubmitView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, exercise_number):
        exercise = Exercise.objects.filter(number=exercise_number, active=True).first()
        if not exercise:
            return Response({'detail': 'Exercise not found.'}, status=status.HTTP_404_NOT_FOUND)

        cycle = get_or_create_daily_cycle(request.user, timezone.localdate())
        state = exercise_state(cycle, exercise)
        if state == 'NOT_ACCESSIBLE_BY_LEVEL':
            return Response({'detail': 'Exercise is not accessible for the current level.'}, status=status.HTTP_403_FORBIDDEN)
        if state == 'BLOCKED_BY_SEQUENCE':
            return Response({'detail': 'Previous exercise must be completed first.'}, status=status.HTTP_409_CONFLICT)

        return Response(
            {'detail': 'Educational validator for this exercise is not configured yet.'},
            status=status.HTTP_501_NOT_IMPLEMENTED,
        )
