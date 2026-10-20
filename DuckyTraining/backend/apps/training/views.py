import random
from datetime import timedelta

from django.db import transaction
from django.db.models import F
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import catalog, validators
from .catalog import CatalogError
from .models import (
    AccessLevel,
    DAILY_LIMITS,
    XP_REWARDS,
    DailyCycle,
    DailyExerciseProgress,
    Exercise,
    SkillProgress,
    TrainingAttempt,
    TrainingStreak,
    UserTrainingProfile,
)


class TrainingConfigurationError(Exception):
    pass


def get_effective_access_level(profile, now=None):
    if profile.access_level == AccessLevel.ALUMNO_PLUS_TEMPORAL:
        now = now or timezone.now()
        if profile.access_expires_at is None or profile.access_expires_at <= now:
            return AccessLevel.FREE
    return profile.access_level


def ensure_cycle_selection(cycle):
    if cycle.selected_exercises.exists():
        return

    active_exercises = Exercise.objects.filter(active=True)
    if cycle.effective_access_level == AccessLevel.FREE:
        free_exercises = list(active_exercises.filter(number__gte=1, number__lte=6))
        if len(free_exercises) < DAILY_LIMITS[AccessLevel.FREE]:
            raise TrainingConfigurationError(
                'El catálogo necesita al menos tres juegos activos numerados del 1 al 6.'
            )
        selected = random.sample(free_exercises, DAILY_LIMITS[AccessLevel.FREE])
    else:
        selected = list(active_exercises.order_by('number'))
        if len(selected) != 10 or [exercise.number for exercise in selected] != list(range(1, 11)):
            raise TrainingConfigurationError(
                'El catálogo debe contener los diez juegos activos numerados del 1 al 10.'
            )

    cycle.selected_exercises.set(selected)
    cycle.daily_limit = len(selected)
    cycle.save(update_fields=['daily_limit'])


@transaction.atomic
def get_or_create_daily_cycle(user, cycle_date):
    profile, _ = UserTrainingProfile.objects.get_or_create(user=user)
    access_level = get_effective_access_level(profile)
    cycle, _ = DailyCycle.objects.get_or_create(
        user=user,
        cycle_date=cycle_date,
        defaults={
            'effective_access_level': access_level,
            'daily_limit': DAILY_LIMITS[access_level],
        },
    )
    cycle = DailyCycle.objects.select_for_update().get(pk=cycle.pk)
    if (
        cycle.effective_access_level == AccessLevel.ALUMNO_PLUS_TEMPORAL
        and access_level == AccessLevel.FREE
    ):
        cycle.effective_access_level = AccessLevel.FREE
        cycle.selected_exercises.clear()
        cycle.daily_limit = DAILY_LIMITS[AccessLevel.FREE]
        cycle.save(update_fields=['effective_access_level', 'daily_limit'])
    ensure_cycle_selection(cycle)
    cycle.completed_count = DailyExerciseProgress.objects.filter(
        cycle=cycle,
        completed=True,
        exercise__in=cycle.selected_exercises.all(),
    ).count()
    cycle.save(update_fields=['completed_count'])
    return cycle


def exercise_state(cycle, exercise):
    if not cycle.selected_exercises.filter(pk=exercise.pk).exists():
        return 'NOT_ACCESSIBLE_BY_LEVEL'

    progress = DailyExerciseProgress.objects.filter(cycle=cycle, exercise=exercise).first()
    if progress and progress.completed:
        return 'COMPLETED_TODAY'
    return 'AVAILABLE'


def public_variant_content(content):
    if content is None:
        return None
    public_content = {
        key: value
        for key, value in content.items()
        if key not in {
            'expected_order',
            'expected_bug_id',
            'expected_connections',
            'explanation',
        }
    }
    if isinstance(public_content.get('steps'), list):
        steps = list(public_content['steps'])
        random.shuffle(steps)
        if len(steps) > 1 and [step['id'] for step in steps] == content.get('expected_order'):
            steps.reverse()
        public_content['steps'] = steps
    return public_content


def update_streak_after_daily_completion(user, cycle, cycle_date):
    if cycle.streak_processed or cycle.completed_count < cycle.daily_limit:
        return

    streak, _ = TrainingStreak.objects.select_for_update().get_or_create(user=user)
    if streak.last_completion_date == cycle_date:
        cycle.streak_processed = True
        cycle.save(update_fields=['streak_processed'])
        return

    if streak.last_completion_date == cycle_date - timedelta(days=1):
        streak.current_streak += 1
    else:
        streak.current_streak = 1
    streak.last_completion_date = cycle_date
    streak.save(update_fields=['current_streak', 'last_completion_date'])
    cycle.streak_processed = True
    cycle.save(update_fields=['streak_processed'])


class TrainingOverviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cycle_date = timezone.localdate()
        try:
            cycle = get_or_create_daily_cycle(request.user, cycle_date)
            exercises = []
            selected_ids = set(cycle.selected_exercises.values_list('id', flat=True))
            for exercise in Exercise.objects.filter(active=True):
                state = exercise_state(cycle, exercise)
                content = None
                if exercise.id in selected_ids:
                    assignment, variant = catalog.get_or_assign_monthly_variant(
                        request.user, exercise, cycle_date.replace(day=1)
                    )
                    content = public_variant_content(variant)
                exercises.append({
                    'number': exercise.number,
                    'name': exercise.logical_name,
                    'type': exercise.exercise_type,
                    'difficulty': exercise.difficulty,
                    'skill': exercise.skill,
                    'state': state if content is not None or state != 'AVAILABLE' else 'CONTENT_PENDING',
                    'content': content,
                })
        except TrainingConfigurationError as exc:
            return Response(
                {'error': 'training_catalog_unavailable', 'message': str(exc)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        except CatalogError as exc:
            return Response(
                {'error': 'training_content_unavailable', 'message': str(exc)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response({
            'access_level': cycle.effective_access_level,
            'daily_limit': cycle.daily_limit,
            'cycle_date': cycle_date,
            'completed_count': cycle.completed_count,
            'xp_per_completed_game': XP_REWARDS[cycle.effective_access_level],
            'xp_grant_status': 'pending_rewards_contract',
            'rewards_status': 'Pendiente de implementar el jueves 22',
            'exercises': exercises,
        })


class ExerciseSubmitView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, exercise_number):
        answer_data = request.data.get('answer')
        if not isinstance(answer_data, dict) or not answer_data:
            return Response({
                'error': 'invalid_request',
                'message': "El campo 'answer' debe ser un objeto JSON no vacío.",
            }, status=status.HTTP_400_BAD_REQUEST)

        exercise = Exercise.objects.filter(number=exercise_number, active=True).first()
        if not exercise:
            return Response(
                {'error': 'invalid_request', 'message': 'Ejercicio no encontrado.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        cycle_date = timezone.localdate()
        try:
            cycle = get_or_create_daily_cycle(request.user, cycle_date)
        except TrainingConfigurationError as exc:
            return Response(
                {'error': 'training_catalog_unavailable', 'message': str(exc)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        state = exercise_state(cycle, exercise)
        if state == 'NOT_ACCESSIBLE_BY_LEVEL':
            return Response(
                {'error': 'exercise_not_accessible', 'message': 'Este juego no forma parte de tu selección diaria.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        progress, _ = DailyExerciseProgress.objects.select_for_update().get_or_create(
            cycle=cycle, exercise=exercise
        )
        current_attempts = TrainingAttempt.objects.filter(
            user=request.user, exercise=exercise, cycle=cycle
        ).count()
        if current_attempts >= 5:
            return Response({
                'error': 'attempt_limit_reached',
                'message': 'Has alcanzado el límite de 5 intentos para este juego hoy.',
            }, status=status.HTTP_409_CONFLICT)

        try:
            assignment, variant_data = catalog.get_or_assign_monthly_variant(
                request.user, exercise, cycle_date.replace(day=1)
            )
        except CatalogError as exc:
            return Response(
                {'error': 'training_content_unavailable', 'message': str(exc)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        if assignment is None or variant_data is None:
            return Response({
                'error': 'educational_content_pending',
                'message': 'El contenido educativo de este juego está pendiente de validación.',
            }, status=status.HTTP_409_CONFLICT)

        if exercise.exercise_type == 'ORDER_ALGORITHM':
            is_correct, explanation = validators.validate_sorting(variant_data, answer_data)
        elif exercise.exercise_type == 'FIND_ERROR':
            is_correct, explanation = validators.validate_bug_finding(variant_data, answer_data)
        elif exercise.exercise_type == 'CONNECT_NETWORK':
            is_correct, explanation = validators.validate_networking(variant_data, answer_data)
        else:
            return Response(
                {'error': 'invalid_exercise_type', 'message': 'Tipo de juego desconocido.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        attempt_number = current_attempts + 1
        TrainingAttempt.objects.create(
            user=request.user,
            exercise=exercise,
            cycle=cycle,
            answer_payload=answer_data,
            is_correct=is_correct,
            error_explanation=explanation,
            variant_reference=assignment.variant_key,
            attempt_number=attempt_number,
        )

        first_completion = is_correct and not progress.completed
        if first_completion:
            progress.completed = True
            progress.completed_at = timezone.now()
            progress.save(update_fields=['completed', 'completed_at'])
            cycle.completed_count = DailyExerciseProgress.objects.filter(
                cycle=cycle,
                completed=True,
                exercise__in=cycle.selected_exercises.all(),
            ).count()
            cycle.save(update_fields=['completed_count'])
            skill_progress, _ = SkillProgress.objects.get_or_create(
                user=request.user, skill=exercise.skill
            )
            SkillProgress.objects.filter(pk=skill_progress.pk).update(
                successful_completions=F('successful_completions') + 1
            )
            update_streak_after_daily_completion(request.user, cycle, cycle_date)

        response_data = {
            'success': True,
            'correct': is_correct,
            'attempt_number': attempt_number,
            'attempts_remaining': 5 - attempt_number,
            'completed': progress.completed,
            'xp_per_completed_game': XP_REWARDS[cycle.effective_access_level],
            'xp_granted': False,
            'xp_grant_status': 'pending_rewards_contract',
            'ducky_coins_granted': False,
        }
        if not is_correct:
            response_data['explanation'] = explanation
        return Response(response_data, status=status.HTTP_200_OK)


class TrainingProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cycle_date = timezone.localdate()
        try:
            cycle = get_or_create_daily_cycle(request.user, cycle_date)
        except TrainingConfigurationError as exc:
            return Response(
                {'error': 'training_catalog_unavailable', 'message': str(exc)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        streak = TrainingStreak.objects.filter(user=request.user).first()
        current_streak = streak.current_streak if streak else 0
        if streak and streak.last_completion_date and streak.last_completion_date < cycle_date - timedelta(days=1):
            current_streak = 0

        skills = SkillProgress.objects.filter(user=request.user).order_by('skill')
        completed_count = DailyExerciseProgress.objects.filter(
            cycle=cycle,
            completed=True,
            exercise__in=cycle.selected_exercises.all(),
        ).count()
        return Response({
            'cycle_date': cycle_date,
            'daily_limit': cycle.daily_limit,
            'completed_count': completed_count,
            'remaining_count': max(cycle.daily_limit - completed_count, 0),
            'xp_per_completed_game': XP_REWARDS[cycle.effective_access_level],
            'xp_grant_status': 'pending_rewards_contract',
            'streak': {
                'current': current_streak,
                'last_completed_date': streak.last_completion_date if streak else None,
                'processed_today': cycle.streak_processed,
            },
            'skills': [
                {
                    'skill': skill.skill,
                    'successful_completions': skill.successful_completions,
                }
                for skill in skills
            ],
        })


class TrainingHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        raw_limit = request.query_params.get('limit', '20')
        try:
            limit = int(raw_limit)
        except (TypeError, ValueError):
            return Response(
                {'error': 'invalid_limit', 'message': 'limit debe ser un entero entre 1 y 100.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not 1 <= limit <= 100:
            return Response(
                {'error': 'invalid_limit', 'message': 'limit debe ser un entero entre 1 y 100.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        attempts = TrainingAttempt.objects.filter(user=request.user).select_related(
            'exercise', 'cycle'
        ).order_by('-submitted_at')[:limit]
        return Response({
            'results': [
                {
                    'exercise_number': attempt.exercise.number,
                    'exercise_name': attempt.exercise.logical_name,
                    'skill': attempt.exercise.skill,
                    'cycle_date': attempt.cycle.cycle_date,
                    'submitted_at': attempt.submitted_at,
                    'attempt_number': attempt.attempt_number,
                    'is_correct': attempt.is_correct,
                    'error_explanation': attempt.error_explanation,
                }
                for attempt in attempts
            ],
            'limit': limit,
        })
