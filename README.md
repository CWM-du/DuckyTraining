# DuckyTraining · Equipo 3

El estado funcional actual, las reglas de acceso, F7, la concesión prevista de XP
y las instrucciones de ejecución están documentados en
[DuckyTraining/README.md](./DuckyTraining/README.md).

**Entorno provisional:** Rewards (validación y evaluación inicial), Rewards
persistente/servicio de procesamiento y Duki Bank/cartera de monedas quedan
«Pendiente de implementar el jueves 22». No se conceden recompensas reales hasta
que los contratos con Equipo 5 estén acordados y disponibles.

El inicio de sesión usa SimpleJWT: `POST /api/token/` devuelve access y refresh;
React incluye el access token como `Authorization: Bearer ...` en las peticiones
protegidas y renueva el access con `POST /api/token/refresh/`.

El seguimiento de tareas y las comprobaciones pendientes están en
[DuckyTraining/docs/TODO.md](./DuckyTraining/docs/TODO.md).
