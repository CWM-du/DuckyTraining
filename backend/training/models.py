from django.conf import settings
from django.db import models


class AccessLevel(models.TextChoices):
    FREE = 'FREE', 'Free'
    ALUMNO_PLUS_TEMPORAL = 'ALUMNO_PLUS_TEMPORAL', 'Alumno con Plus temporal'
    PLUS = 'PLUS', 'Plus'
    PRO = 'PRO', 'Pro'


DAILY_LIMITS = {
    AccessLevel.FREE: 3,
    AccessLevel.ALUMNO_PLUS_TEMPORAL: 5,
    AccessLevel.PLUS: 7,
    AccessLevel.PRO: 10,
}


class ExerciseType(models.TextChoices):
    ORDER_ALGORITHM = 'ORDER_ALGORITHM', 'Ordena el algoritmo'
    FIND_ERROR = 'FIND_ERROR', 'Encuentra el fallo'
    CONNECT_NETWORK = 'CONNECT_NETWORK', 'Conecta la red'


class Difficulty(models.TextChoices):
    EASY = 'EASY', 'Fácil'
    MEDIUM = 'MEDIUM', 'Media'
    HARD = 'HARD', 'Difícil'


class Exercise(models.Model):
    number = models.PositiveSmallIntegerField(unique=True)
    logical_name = models.CharField(max_length=150)
    exercise_type = models.CharField(max_length=32, choices=ExerciseType.choices, null=True, blank=True)
    difficulty = models.CharField(max_length=16, choices=Difficulty.choices)
    skill = models.CharField(max_length=120)
    introductory_relation = models.CharField(max_length=180)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['number']


class UserTrainingProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # TEMP_REPLACE: sustituible por el contrato oficial de Equipos 0/5.
    access_level = models.CharField(max_length=32, choices=AccessLevel.choices, default=AccessLevel.FREE)


class MonthlyVariantAssignment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    month = models.DateField(help_text='Primer día del mes de asignación')
    variant_key = models.CharField(max_length=100)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'exercise', 'month'], name='unique_training_month_variant')]


class DailyCycle(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cycle_date = models.DateField()
    effective_access_level = models.CharField(max_length=32, choices=AccessLevel.choices)
    daily_limit = models.PositiveSmallIntegerField()
    completed_count = models.PositiveSmallIntegerField(default=0)
    final_reward_processed = models.BooleanField(default=False)
    streak_processed = models.BooleanField(default=False)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'cycle_date'], name='unique_training_daily_cycle')]


class DailyExerciseProgress(models.Model):
    cycle = models.ForeignKey(DailyCycle, on_delete=models.CASCADE, related_name='exercise_progress')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    xp_reward_processed = models.BooleanField(default=False)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['cycle', 'exercise'], name='unique_training_daily_exercise')]


class TrainingAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    cycle = models.ForeignKey(DailyCycle, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    answer_payload = models.JSONField()
    is_correct = models.BooleanField()
    error_explanation = models.TextField(blank=True)


class SkillProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    skill = models.CharField(max_length=120)
    successful_completions = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'skill'], name='unique_training_skill_progress')]


class TrainingStreak(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    current_streak = models.PositiveIntegerField(default=0)
    last_completion_date = models.DateField(null=True, blank=True)


class TrainingAchievement(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    achievement_key = models.CharField(max_length=100)
    granted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'achievement_key'], name='unique_training_achievement')]
