# Fase 7 · Progreso e historial

## Implementado en el entorno provisional

- Los intentos validados se guardan en `TrainingAttempt`, incluidos los fallos y
  reintentos. El historial se limita a los intentos del usuario autenticado.
- La primera finalización correcta de un juego durante el ciclo incrementa
  `SkillProgress.successful_completions` para la habilidad del juego. Un acierto
  repetido el mismo día se conserva en historial, pero no incrementa dos veces el
  progreso de habilidad.
- `DailyCycle.completed_count` refleja los juegos distintos seleccionados que se
  completaron en el ciclo.
- La racha avanza una sola vez al completar toda la selección diaria; el endpoint
  devuelve cero si la última finalización fue anterior al día local de ayer.
- `GET /api/training/progress/` devuelve progreso por habilidad, cupo y racha.
- `GET /api/training/history/?limit=20` devuelve los intentos más recientes; acepta
  límites de 1 a 100. Ambas vistas exigen autenticación y filtran por `request.user`.
- React consulta estas rutas y muestra progreso e historial.

## XP, Rewards y monedas

- Regla definida: 5 XP por juego completado para Free, Plus, Pro y Alumno Plus
  temporal vigente.
- La concesión no está activa: la API comunica que XP no fue concedido y tampoco
  concede Duki Coins. El estado de procesamiento permanece pendiente.
- Rewards (validación/evaluación inicial y persistencia/servicio de procesamiento)
  y Duki Bank/cartera de monedas: **pendiente de implementar el jueves 22**.
- Los logros se conservan sin lógica de concesión en esta fase.

## Pruebas

La suite incluye casos para selección y acceso, caducidad temporal, límite de
intentos, ausencia de concesiones reales, progreso por habilidad, racha e
aislamiento de historial/progreso. Ejecutar desde `backend`:

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test apps.training
```

La ejecución de esas comprobaciones queda pendiente; no se afirma que hayan pasado.
