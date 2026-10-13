# Rutas · Equipo 3 · DuckyTraining

| Método | Ruta | Propósito | Auth |
|---|---|---|---|
| GET | `/api/training/overview/` | Estado del ciclo y ejercicios del usuario | Sí |
| POST | `/api/training/exercises/<exercise_number>/submit/` | Envío de respuesta de un ejercicio | Sí |
| GET/POST/etc. | `/admin/` | Administración Django de datos de Training | Superusuario |

## Reglas

- Las URLs se centralizan en `config/urls.py` y `apps.training/urls.py`.
- La validación educativa definitiva no está implementada hasta disponer del contenido aprobado.
- El cliente no determina corrección, XP ni DuckyCoins.
