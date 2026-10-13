from django.contrib import admin
from .models import (
    DailyCycle, DailyExerciseProgress, Exercise, MonthlyVariantAssignment,
    SkillProgress, TrainingAchievement, TrainingAttempt, TrainingStreak, UserTrainingProfile,
)

admin.site.register([
    Exercise, UserTrainingProfile, MonthlyVariantAssignment, DailyCycle,
    DailyExerciseProgress, TrainingAttempt, SkillProgress, TrainingStreak,
    TrainingAchievement,
])
