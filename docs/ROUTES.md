# Rutas · Equipo 3 · DuckyTraining

| Método | Ruta | Propósito | Auth |
|---|---|---|---|
| GET | `/api/training/` | Estado del ciclo, selección diaria y juegos disponibles | Sí |
| GET | `/api/training/progress/` | Progreso por habilidad, cupo diario y racha del usuario | Sí |
| GET | `/api/training/history/?limit=20` | Últimos intentos del usuario; límite permitido de 1–100 | Sí |
| POST | `/api/training/exercises/<exercise_number>/submit/` | Envío de respuesta de un ejercicio | Sí |
| GET/POST/etc. | `/admin/` | Administración Django de datos de Training | Superusuario |

## Reglas

- Las URLs se centralizan en `config/urls.py` y `apps.training/urls.py`.
- Los endpoints de progreso e historial filtran los registros por el usuario autenticado.
- El progreso por habilidad aumenta una sola vez por juego y ciclo diario; los reintentos posteriores permanecen en el historial.
- La racha solo se actualiza al completar todo el cupo diario disponible, usando la fecha local `Europe/Madrid`.
- No se implementan logros, XP ni Duki Coins en F7; esperan reglas o contratos aprobados.
- La validación educativa definitiva requiere contenido aprobado y publicado.
- El cliente no determina la corrección ni gestiona XP o Duki Coins.
