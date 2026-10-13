# Lógica aplicada

La implementación inicial sigue `logica.md` como especificación funcional de Equipo 3.

No se han inventado preguntas, respuestas, explicaciones, cantidades de recompensa ni contratos externos.

El código contiene puntos explícitos de sustitución para la integración futura con Equipos 0 y 5.


## Reglas F6 aplicadas

- `Europe/Madrid` determina la fecha local de los ciclos diarios.
- FREE recibe tres juegos aleatorios entre los números 1–6, persistidos en `DailyCycle.selected_exercises`.
- PLUS y PRO acceden a los diez juegos sin bloqueo secuencial.
- `ALUMNO_PLUS_TEMPORAL` mantiene temporalmente el comportamiento heredado hasta la confirmación de Equipo 0.
- Las recompensas reales no se simulan; XP y Duki Coins se conectarán con sus contratos oficiales.
