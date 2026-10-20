# Equipo 3 · DuckyTraining

Módulo individual de práctica de DuckyWorld/DuckyArenas. El estado actual es un
entorno virtual provisional; no representa una integración de recompensas real.

## Implementado

- Catálogo lógico de diez juegos.
- Ciclo diario individual con fecha local `Europe/Madrid`.
- Free recibe tres juegos aleatorios de los juegos 1–6, persistidos durante el ciclo.
- Plus, Pro y Alumno Plus temporal vigente reciben los diez juegos. El acceso temporal
  solo está vigente si `access_expires_at` está definido y es posterior a la hora actual.
- Los juegos seleccionados no requieren desbloqueo secuencial.
- Límite de cinco intentos por juego y ciclo diario.
- Progreso por habilidad: una suma por primera finalización correcta de cada juego
  durante el ciclo.
- Racha: se procesa una vez al completar todos los juegos seleccionados para el día.
- `GET /api/training/progress/` y `GET /api/training/history/?limit=20`, protegidos
  por autenticación y limitados al usuario autenticado.
- Autenticación SimpleJWT: `POST /api/token/` recibe `username` y `password`, y
  devuelve `access` y `refresh`; `POST /api/token/refresh/` renueva el access token.
  React guarda ambos tokens en `sessionStorage` y envía `Authorization: Bearer ...`
  a las rutas protegidas.
- XP previsto de 5 por juego completado para Free, Plus, Pro y Alumno Plus temporal
  vigente. El código no concede ni persiste XP real hasta disponer del contrato.
- Modelos sincronizados con las migraciones, incluida la selección diaria, el estado
  separado de procesamiento de XP/monedas y la caducidad del acceso temporal.
- El frontend consulta Training, progreso e historial al backend; no presenta saldos
  ficticios ni decide aleatoriamente si una respuesta es correcta.

## Pendiente de implementar el jueves 22

Se mantiene el entorno virtual provisional. No se conceden recompensas reales:

- **Rewards: validación y evaluación inicial.**
- **Rewards persistente y servicio de procesamiento.**
- **Duki Bank y cartera de monedas.**

La concesión de 5 XP está definida como regla de producto, pero su procesamiento
queda desactivado hasta que el contrato de Rewards y el servicio de Duki Bank estén
disponibles y acordados con Equipo 5. Las respuestas de la API indican explícitamente
que XP y Duki Coins no se han concedido.

## Pendiente de contenido educativo e integración

- Preparar y aprobar enunciados, soluciones y explicaciones de las diez actividades.
- Publicar variantes educativas válidas en `backend/apps/training/content/catalog.json`.
  Mientras no haya variantes publicadas, el juego se muestra como pendiente y el
  backend no simula una respuesta.
- Acordar con Equipo 5 los contratos de Rewards/Duki Bank y la idempotencia del
  procesamiento antes de activar cualquier concesión.
- Conectar la identidad y el acceso del entorno con los contratos de los equipos
  correspondientes; `UserTrainingProfile` sigue siendo una fuente provisional.

## Ejecución local

### Backend

Desde `backend`:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_logical_exercises
python manage.py runserver
```

### Frontend

Desde `frontend`:

```powershell
npm install
npm run dev
```

La interfaz usa `VITE_TRAINING_API_URL` si está configurada; por defecto consulta
`http://localhost:8000/api/training`. Para cambiar solo el prefijo API, configura
`VITE_API_BASE_URL` (por defecto `http://localhost:8000/api`); el login y refresh
usan ese mismo prefijo.
