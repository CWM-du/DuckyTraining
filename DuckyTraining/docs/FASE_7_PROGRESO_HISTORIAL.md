# Fase 7 · Progreso e historial

## Implementado en esta revisión

- Cada intento validado se conserva en `TrainingAttempt`, tanto si es correcto como incorrecto. Los reintentos posteriores siguen apareciendo en el historial.
- Una primera finalización correcta de un juego dentro del ciclo diario incrementa `SkillProgress.successful_completions` una sola vez para la habilidad de ese juego. Volver a acertar el mismo juego ese día no vuelve a incrementar el progreso.
- `DailyCycle.completed_count` se sincroniza con el número de juegos distintos completados en el ciclo.
- La racha se actualiza una sola vez al completar el cupo diario disponible: selección de Free, catálogo activo completo para Plus/Pro o cupo heredado para `ALUMNO_PLUS_TEMPORAL`. Las fechas usan `timezone.localdate()` con la zona `Europe/Madrid`.
- Si la última racha registrada fue anterior al día local de ayer, el endpoint de progreso informa una racha actual de cero. El historial de la última finalización se conserva.
- `GET /api/training/progress/` devuelve progreso por habilidad, estado del cupo y racha del usuario autenticado.
- `GET /api/training/history/?limit=20` devuelve los últimos intentos del usuario autenticado; el límite permitido es de 1 a 100. Las consultas filtran siempre por `request.user`.
- React consulta y muestra progreso, habilidades e historial a través de `trainingApi.js`.

## Fuera de alcance por decisión explícita

- XP y Duki Coins: no se calculan ni se envían a servicios externos. Requieren los contratos aprobados de Ecomotor y Duki Bank/Equipo 5.
- Logros: no se conceden ni se definen hitos en esta fase, a la espera de reglas aprobadas. El modelo existente se conserva sin lógica nueva.
- No se ha añadido migración: esta implementación reutiliza los modelos y campos existentes.

## Pruebas añadidas; ejecución pendiente del usuario

- Actualización de progreso por habilidad tras un primer acierto.
- Reintento correcto registrado en historial sin duplicar el progreso de habilidad.
- Endpoints de progreso e historial limitados al usuario autenticado.
- Validación del límite de historial.
- Racha que no se actualiza antes de completar el cupo, se procesa una sola vez y continúa en días consecutivos.

Ejecutar en el entorno virtual del proyecto desde `backend`:

```powershell
py -3.15 manage.py makemigrations --check --dry-run
py -3.15 manage.py check
py -3.15 manage.py test apps.training
```

No se han ejecutado comandos Django ni tests durante la preparación de este ZIP.
