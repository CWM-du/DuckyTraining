from django.urls import path
from .views import (
    ExerciseSubmitView,
    ProvidedGameChallengeView,
    ProvidedGamesView,
    TrainingHistoryView,
    TrainingOverviewView,
    TrainingProgressView,
)

urlpatterns = [
    path('', TrainingOverviewView.as_view(), name='training-overview'),
    path('provided-games/', ProvidedGamesView.as_view(), name='provided-games'),
    path(
        'provided-games/<slug:game_id>/<int:level>/',
        ProvidedGameChallengeView.as_view(),
        name='provided-game-challenge',
    ),
    path('exercises/<int:exercise_number>/submit/', ExerciseSubmitView.as_view(), name='training-exercise-submit'),
    path('progress/', TrainingProgressView.as_view(), name='training-progress'),
    path('history/', TrainingHistoryView.as_view(), name='training-history'),
]
