from django.db import models
from django.conf import settings

class ProfileUserTraining(models.Model):
    LEVEL_CHOICES = [
        ('FREE', 'Free'),
        ('ALUMNO_PLUS_TEMPORAL', 'Alumno con Plus temporal'),
        ('PLUS', 'Plus de pago'),
        ('PRO', 'Pro de pago'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='training_profile'
    )
    
    temporal_level = models.CharField(
        max_length=50,  # Aumentado un poco por si el Equipo 0 crea roles con nombres largos a futuro
        choices=LEVEL_CHOICES,
        default='FREE',
        help_text="Nivel de acceso temporal hasta la integración con Equipos 0 y 5"
    )
    
    current_streak = models.PositiveIntegerField(
        default=0,
        help_text="Días consecutivos completando el cupo diario"
    )
    last_streak_date = models.DateField(
        null=True, 
        blank=True,
        help_text="Última fecha en la que completó el cupo para calcular la racha"
    )

    # 💡 MEJORA 1: Campos de auditoría silenciosos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Training Profile - {self.user.username}"

    # 💡 MEJORA 2: Encapsulación del cupo diario
    @property
    def daily_quota(self):
        """
        Devuelve la cantidad de ejercicios permitidos según el nivel temporal.
        Evita tener que reescribir esta lógica en las vistas o serializadores.
        """
        quotas = {
            'FREE': 3,
            'ALUMNO_PLUS_TEMPORAL': 5,
            'PLUS': 7,
            'PRO': 10
        }
        return quotas.get(self.temporal_level, 3) # 3 por defecto por seguridad