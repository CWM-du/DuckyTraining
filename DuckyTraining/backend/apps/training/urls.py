from django.urls import path
from .views import (TrainingOverviewView, ExerciseSubmitView, TrainingProgressView, TrainingHistoryView)

urlpatterns = [
    path('', TrainingOverviewView.as_view(), name='training-overview'),
    path('progress/', TrainingProgressView.as_view(), name='training-progress'),
    path('history/', TrainingHistoryView.as_view(), name='training-history'),
    path('exercises/<int:exercise_number>/submit/', ExerciseSubmitView.as_view(), name='training-exercise-submit'),
]
