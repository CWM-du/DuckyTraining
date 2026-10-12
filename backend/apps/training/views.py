from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    AccessLevel, DAILY_LIMITS, DailyCycle, DailyExerciseProgress, Exercise,
    TrainingAttempt, UserTrainingProfile, MonthlyVariantAssignment
)
from . import validators


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
        answer_data = request.data.get('answer')
        if not answer_data:
            return Response({
                "error": "invalid_request",
                "message": "Falta el campo 'answer'."
            }, status=status.HTTP_400_BAD_REQUEST)

        exercise = Exercise.objects.filter(number=exercise_number, active=True).first()
        if not exercise:
            return Response({'error': 'invalid_request', 'message': 'Ejercicio no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        today = timezone.localdate()
        cycle = get_or_create_daily_cycle(request.user, today)
        
        # Validación de secuencia de tu código original
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

        # Recuperar variante (Punto 5)
        first_day_of_month = today.replace(day=1)
        assignment = MonthlyVariantAssignment.objects.filter(
            user=request.user, exercise=exercise, month=first_day_of_month
        ).first()

        if not assignment:
            return Response({
                "error": "variant_not_found",
                "message": "No existe una variante disponible para este ejercicio."
            }, status=status.HTTP_404_NOT_FOUND)

        # Simulación de datos del JSON que vendrá en la variante
        variant_data = {} 
        variant_key = assignment.variant_key
        
        # Delegar en validators modulares (Punto 8)
        is_correct, explanation = False, ""
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
            progress.save()

            # Actualizamos contador del ciclo
            cycle.completed_count += 1
            cycle.save()

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