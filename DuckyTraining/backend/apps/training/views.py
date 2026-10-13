import random
from datetime import timedelta

from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    AccessLevel, DAILY_LIMITS, DailyCycle, DailyExerciseProgress, Exercise,
    SkillProgress, TrainingAttempt, TrainingStreak, UserTrainingProfile, MonthlyVariantAssignment
)
from . import validators
from .catalog import CatalogError, get_or_assign_monthly_variant


def _daily_limit_for_access(access_level):
    return DAILY_LIMITS.get(access_level, DAILY_LIMITS[AccessLevel.FREE])


def get_or_create_daily_cycle(user, cycle_date):
    """Create today's cycle and persist FREE's random selection exactly once."""
    with transaction.atomic():
        profile, _ = UserTrainingProfile.objects.get_or_create(user=user)
        cycle, _ = DailyCycle.objects.get_or_create(
            user=user,
            cycle_date=cycle_date,
            defaults={
                'effective_access_level': profile.access_level,
                'daily_limit': _daily_limit_for_access(profile.access_level),
            },
        )
        # Row locking protects one-time selection on database engines that support it.
        cycle = DailyCycle.objects.select_for_update().get(pk=cycle.pk)
        # Normalize cycles created earlier today under the previous 3/5/7/10 rules.
        expected_limit = _daily_limit_for_access(cycle.effective_access_level)
        if cycle.daily_limit != expected_limit:
            cycle.daily_limit = expected_limit
            cycle.save(update_fields=['daily_limit'])
        if cycle.effective_access_level == AccessLevel.FREE and not cycle.selected_exercises.exists():
            candidate_exercises = list(
                Exercise.objects.filter(active=True, number__gte=1, number__lte=6).order_by('number')
            )
            selected = random.sample(candidate_exercises, k=min(3, len(candidate_exercises)))
            if selected:
                cycle.selected_exercises.set(selected)
        return cycle



def daily_quota_count(cycle):
    """Return the number of distinct active games required for this cycle's quota."""
    active = Exercise.objects.filter(active=True)
    if cycle.effective_access_level == AccessLevel.FREE:
        return cycle.selected_exercises.filter(active=True).count()
    if cycle.effective_access_level in (AccessLevel.PLUS, AccessLevel.PRO):
        return active.count()
    if cycle.effective_access_level == AccessLevel.ALUMNO_PLUS_TEMPORAL:
        return active.filter(number__lte=cycle.daily_limit).count()
    return 0


def update_streak_if_quota_complete(cycle, today):
    """Update a user's streak once, only after all games in the daily quota are completed."""
    if cycle.streak_processed:
        return False

    quota = daily_quota_count(cycle)
    if quota <= 0:
        return False

    completed = DailyExerciseProgress.objects.filter(cycle=cycle, completed=True).count()
    if completed < quota:
        return False

    streak, _ = TrainingStreak.objects.select_for_update().get_or_create(user=cycle.user)
    if streak.last_completion_date == today:
        # Idempotency guard in case the cycle flag was not persisted by an older version.
        cycle.streak_processed = True
        cycle.save(update_fields=['streak_processed'])
        return False

    if streak.last_completion_date == today - timedelta(days=1):
        streak.current_streak += 1
    else:
        streak.current_streak = 1
    streak.last_completion_date = today
    streak.save(update_fields=['current_streak', 'last_completion_date'])

    cycle.streak_processed = True
    cycle.save(update_fields=['streak_processed'])
    return True

def exercise_state(cycle, exercise):
    progress = DailyExerciseProgress.objects.filter(cycle=cycle, exercise=exercise).first()

    if cycle.effective_access_level == AccessLevel.FREE:
        if not cycle.selected_exercises.filter(pk=exercise.pk).exists():
            return 'NOT_ACCESSIBLE_BY_LEVEL'
        return 'COMPLETED_TODAY' if progress and progress.completed else 'AVAILABLE'

    if cycle.effective_access_level in (AccessLevel.PLUS, AccessLevel.PRO):
        # Plus and Pro can open any active exercise; there is no sequential lock.
        return 'COMPLETED_TODAY' if progress and progress.completed else 'AVAILABLE'

    if cycle.effective_access_level == AccessLevel.ALUMNO_PLUS_TEMPORAL:
        # Legacy-only behavior, retained unchanged until Equipo 0 defines conversion.
        if exercise.number > cycle.daily_limit:
            return 'NOT_ACCESSIBLE_BY_LEVEL'
        if progress and progress.completed:
            return 'COMPLETED_TODAY'
        if exercise.number == 1:
            return 'AVAILABLE'
        previous_completed = DailyExerciseProgress.objects.filter(
            cycle=cycle, exercise__number=exercise.number - 1, completed=True
        ).exists()
        return 'AVAILABLE' if previous_completed else 'BLOCKED_BY_SEQUENCE'

    return 'NOT_ACCESSIBLE_BY_LEVEL'


class TrainingOverviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cycle_date = timezone.localdate()
        cycle = get_or_create_daily_cycle(request.user, cycle_date)
        exercises = []
        for exercise in Exercise.objects.filter(active=True):
            state = exercise_state(cycle, exercise)
            exercises.append({
                'number': exercise.number,
                'name': exercise.logical_name,
                'type': exercise.exercise_type,
                'difficulty': exercise.difficulty,
                'skill': exercise.skill,
                'state': state,
                'selected_today': (
                    cycle.selected_exercises.filter(pk=exercise.pk).exists()
                    if cycle.effective_access_level == AccessLevel.FREE
                    else state != 'NOT_ACCESSIBLE_BY_LEVEL'
                ),
            })
        return Response({
            'access_level': cycle.effective_access_level,
            'daily_limit': cycle.daily_limit,
            'cycle_date': cycle_date,
            'selected_exercise_numbers': list(
                cycle.selected_exercises.order_by('number').values_list('number', flat=True)
            ),
            'access_rule': (
                'Tres juegos seleccionados aleatoriamente entre los juegos 1–6.'
                if cycle.effective_access_level == AccessLevel.FREE
                else 'Catálogo completo de diez juegos.'
                if cycle.effective_access_level in (AccessLevel.PLUS, AccessLevel.PRO)
                else 'Estado heredado: cinco juegos secuenciales hasta confirmación de Equipo 0.'
            ),
            'completed_count': cycle.completed_count,
            'exercises': exercises,
        })


class TrainingProgressView(APIView):
    """Read-only progress summary scoped strictly to the authenticated user."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.localdate()
        cycle = get_or_create_daily_cycle(request.user, today)
        skills = list(
            SkillProgress.objects.filter(user=request.user)
            .order_by('skill')
            .values('skill', 'successful_completions')
        )
        streak = TrainingStreak.objects.filter(user=request.user).first()
        current_streak = streak.current_streak if streak else 0
        last_completion_date = streak.last_completion_date if streak else None
        # A streak is no longer current after a full missed local day. Keep stored history intact.
        if last_completion_date and last_completion_date < today - timedelta(days=1):
            current_streak = 0

        quota = daily_quota_count(cycle)
        completed = DailyExerciseProgress.objects.filter(cycle=cycle, completed=True).count()
        return Response({
            'cycle_date': today,
            'completed_count': completed,
            'daily_quota': quota,
            'daily_quota_complete': quota > 0 and completed >= quota,
            'skills': skills,
            'streak': {
                'current_streak': current_streak,
                'last_completion_date': last_completion_date,
            },
        })


class TrainingHistoryView(APIView):
    """Return only the authenticated user's own attempt history."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        raw_limit = request.query_params.get('limit', '50')
        try:
            limit = int(raw_limit)
        except (TypeError, ValueError):
            return Response(
                {'error': 'invalid_limit', 'message': "El parámetro 'limit' debe ser un entero."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if limit < 1 or limit > 100:
            return Response(
                {'error': 'invalid_limit', 'message': "El parámetro 'limit' debe estar entre 1 y 100."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        attempts = (
            TrainingAttempt.objects.filter(user=request.user)
            .select_related('exercise', 'cycle')
            .order_by('-submitted_at', '-pk')[:limit]
        )
        return Response({
            'count': len(attempts),
            'results': [
                {
                    'id': attempt.pk,
                    'exercise_number': attempt.exercise.number,
                    'exercise_name': attempt.exercise.logical_name,
                    'cycle_date': attempt.cycle.cycle_date,
                    'submitted_at': attempt.submitted_at,
                    'attempt_number': attempt.attempt_number,
                    'is_correct': attempt.is_correct,
                    'answer': attempt.answer_payload,
                    'explanation': attempt.error_explanation,
                    'variant_reference': attempt.variant_reference,
                }
                for attempt in attempts
            ],
        })


class ExerciseSubmitView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, exercise_number):
        answer_data = request.data.get('answer')
        if not isinstance(answer_data, dict) or not answer_data:
            return Response({
                "error": "invalid_request",
                "message": "Falta el campo 'answer'."
            }, status=status.HTTP_400_BAD_REQUEST)

        exercise = Exercise.objects.filter(number=exercise_number, active=True).first()
        if not exercise:
            return Response({'error': 'invalid_request', 'message': 'Ejercicio no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        today = timezone.localdate()
        cycle = get_or_create_daily_cycle(request.user, today)
        # Serializa envíos del mismo usuario/ciclo en motores que soportan row locks.
        # SQLite no ofrece la misma garantía; verificar concurrencia en el entorno final.
        cycle = DailyCycle.objects.select_for_update().get(pk=cycle.pk)

        # F6: Free juega solo los seleccionados; Plus/Pro no tienen secuencia obligatoria.
        # El estado ALUMNO_PLUS_TEMPORAL conserva temporalmente la regla heredada.
        state = exercise_state(cycle, exercise)
        if state == 'NOT_ACCESSIBLE_BY_LEVEL':
            return Response({'error': 'invalid_request', 'message': 'No accesible por nivel.'}, status=status.HTTP_403_FORBIDDEN)
        if state == 'BLOCKED_BY_SEQUENCE':
            return Response({'error': 'invalid_request', 'message': 'Debes completar el anterior.'}, status=status.HTTP_409_CONFLICT)

        # BLOQUEO ANTI-CONCURRENCIA (Punto 16 de F5)
        # Aseguramos el progreso para evitar clics dobles simultáneos
        progress, _ = DailyExerciseProgress.objects.select_for_update().get_or_create(
            cycle=cycle, exercise=exercise
        )

        # Control de 5 intentos máximo
        current_attempts = TrainingAttempt.objects.filter(user=request.user, exercise=exercise, cycle=cycle).count()
        if current_attempts >= 5:
            return Response({
                "error": "attempt_limit_reached",
                "message": "Has alcanzado el límite de 5 intentos para este juego hoy."
            }, status=status.HTTP_409_CONFLICT)

        # Recuperar/asignar una variante mensual publicada desde el catálogo JSON.
        first_day_of_month = today.replace(day=1)
        try:
            assignment, variant_data = get_or_assign_monthly_variant(
                request.user, exercise, first_day_of_month
            )
        except CatalogError as exc:
            return Response({
                'error': 'catalog_configuration_error',
                'message': str(exc),
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        if assignment is None or variant_data is None:
            return Response({
                'error': 'variant_content_pending',
                'message': 'Este juego aún no tiene una variante educativa publicada y validada.',
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        variant_key = assignment.variant_key

        # Delegar en validadores modulares. El contenido procede del catálogo del servidor.
        if exercise.exercise_type == 'ORDER_ALGORITHM':
            is_correct, explanation = validators.validate_sorting(variant_data, answer_data)
        elif exercise.exercise_type == 'FIND_ERROR':
            is_correct, explanation = validators.validate_bug_finding(variant_data, answer_data)
        elif exercise.exercise_type == 'CONNECT_NETWORK':
            is_correct, explanation = validators.validate_networking(variant_data, answer_data)
        else:
            return Response({"error": "invalid_request", "message": "Tipo de juego desconocido."}, status=status.HTTP_400_BAD_REQUEST)

        # Registrar intento
        attempt_number = current_attempts + 1
        TrainingAttempt.objects.create(
            user=request.user,
            exercise=exercise,
            cycle=cycle,
            answer_payload=answer_data,
            is_correct=is_correct,
            error_explanation=explanation,
            variant_reference=variant_key,
            attempt_number=attempt_number
        )

        # Actualizar progreso si acierta
        if is_correct and not progress.completed:
            progress.completed = True
            progress.completed_at = timezone.now()
            progress.save(update_fields=['completed', 'completed_at'])

            # F7: una sola finalización por juego y ciclo suma progreso a la habilidad.
            skill_progress, _ = SkillProgress.objects.select_for_update().get_or_create(
                user=request.user, skill=exercise.skill
            )
            skill_progress.successful_completions += 1
            skill_progress.save(update_fields=['successful_completions'])

            # El contador cuenta juegos distintos completados, no intentos.
            cycle.completed_count = DailyExerciseProgress.objects.filter(
                cycle=cycle, completed=True
            ).count()
            cycle.save(update_fields=['completed_count'])

        if is_correct:
            update_streak_if_quota_complete(cycle, today)

        # Respuesta estructurada según contrato F5
        response_data = {
            "success": True,
            "correct": is_correct,
            "attempt_number": attempt_number,
            "attempts_remaining": 5 - attempt_number,
            "completed": progress.completed
        }
        if not is_correct:
            response_data["explanation"] = explanation

        return Response(response_data, status=status.HTTP_200_OK)