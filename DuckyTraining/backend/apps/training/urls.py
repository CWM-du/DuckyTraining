from django.urls import path
from .views import (
    ExerciseSubmitView,
    TrainingHistoryView,
    TrainingOverviewView,
    TrainingProgressView,
)

urlpatterns = [
    path('', TrainingOverviewView.as_view(), name='training-overview'),
    path('exercises/<int:exercise_number>/submit/', ExerciseSubmitView.as_view(), name='training-exercise-submit'),
    path('progress/', TrainingProgressView.as_view(), name='training-progress'),
    path('history/', TrainingHistoryView.as_view(), name='training-history'),
]
