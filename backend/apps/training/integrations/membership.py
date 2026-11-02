"""Interfaz provisional de membresía. La fuente oficial corresponde a Equipo 0/Core."""
from django.utils import timezone

from .config import load_integration_config
from ..models import AccessLevel, UserTrainingProfile


def get_membership_for_training(user, now=None):
    """Devuelve membresía local provisional; no afirma ser identidad oficial."""
    config = load_integration_config()
    profile, _ = UserTrainingProfile.objects.get_or_create(user=user)
    level = profile.access_level
    if level == AccessLevel.ALUMNO_PLUS_TEMPORAL:
        now = now or timezone.now()
        expiry = profile.access_expires_at
        if expiry is None or expiry <= now:
            level = AccessLevel.FREE
    if level not in config['access_levels']:
        return AccessLevel.FREE
    return level
