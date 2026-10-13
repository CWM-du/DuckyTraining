# Equipo 3 · DuckyTraining

Módulo individual de práctica de DuckyWorld/DuckyArenas.

## Estado actual

- F4 y F5: concluidas en su estado estructural; el contenido educativo real se incorporará a futuro.
- F6: corrección estructural implementada, pendiente de comprobación en el entorno virtual del usuario.
- FREE: tres juegos seleccionados aleatoriamente entre los juegos 1–6, con selección persistente durante el día.
- PLUS/PRO: acceso al catálogo completo de diez juegos, sin bloqueo secuencial.
- `ALUMNO_PLUS_TEMPORAL`: estado heredado conservado con sus cinco juegos secuenciales hasta que Equipo 0 confirme la conversión.
- Ciclo diario y fecha local basados en `Europe/Madrid`.

## Stack

- Frontend: React + Vite
- Backend: Python + Django + Django REST Framework
- Base de desarrollo: SQLite

## Validación local de F6

Desde `DuckyTraining/backend`, con el entorno virtual existente activado, ejecutar en PowerShell:

```powershell
py -3.15 manage.py makemigrations --check --dry-run
py -3.15 manage.py check
py -3.15 manage.py migrate
py -3.15 manage.py test apps.training
```

No se han ejecutado comandos Django al preparar esta versión. Ver `DuckyTraining/docs/FASE_6_CICLO_DIARIO.md` para las reglas y los límites pendientes.

## Límites conocidos

- El cambio de membresía durante el día requiere el contrato de Equipo 0/Ecomotor.
- El envío real de XP y Duki Coins requiere los contratos oficiales de Ecomotor y Duki Bank/Equipo 5; no se simulan.
- Las pruebas de concurrencia deben validarse con el motor de base de datos de despliegue; SQLite no ofrece las mismas garantías de bloqueo de fila que PostgreSQL.
- Las variantes educativas siguen pendientes por decisión del equipo.
