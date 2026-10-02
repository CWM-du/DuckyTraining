from django.urls import path
from .views import TrainingOverviewView, ExerciseSubmitView

urlpatterns = [
    path('', TrainingOverviewView.as_view(), name='training-overview'),
    path('exercises/<int:exercise_number>/submit/', ExerciseSubmitView.as_view(), name='training-exercise-submit'),
]
