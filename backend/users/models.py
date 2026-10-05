from django.db import models
from django.conf import settings

class ProfileUserTraining(models.Model):
    LEVEL_CHOICES = [
        ('FREE', 'Free'),
        ('ALUMNO_PLUS_TEMPORAL', 'Alumno con Plus temporal'),
        ('PLUS', 'Plus de pago'),
        ('PRO', 'Pro de pago'),
    ]

    # Relación OneToOne con el User del proyecto principal (Equipo 0 / Profesor)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='training_profile'
    )
    
    # Nivel temporal según el documento funcional
    temporal_level = models.CharField(
        max_length=25,
        choices=LEVEL_CHOICES,
        default='FREE',
        help_text="Nivel de acceso temporal hasta la integración con Equipos 0 y 5"
    )
    
    # Gestión de rachas
    current_streak = models.PositiveIntegerField(
        default=0,
        help_text="Días consecutivos completando el cupo diario"
    )
    last_streak_date = models.DateField(
        null=True, 
        blank=True,
        help_text="Última fecha en la que completó el cupo para calcular la racha"
    )

    def __str__(self):
        return f"Training Profile - {self.user.username}"