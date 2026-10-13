# Fase 6 · Ciclo diario y acceso

## Reglas implementadas

- Zona horaria del proyecto: `Europe/Madrid`; `timezone.localdate()` determina la fecha local del ciclo y de los intentos diarios.
- FREE: el backend elige hasta tres juegos activos entre los números 1–6 al crear el ciclo. La relación `DailyCycle.selected_exercises` persiste la selección para que las consultas posteriores del mismo día no vuelvan a sortearla. Con el catálogo normal de diez juegos, se seleccionan tres.
- PLUS y PRO: los diez juegos activos son accesibles y no existe bloqueo por secuencia. `daily_limit=10` representa el tamaño del catálogo definido actualmente.
- `ALUMNO_PLUS_TEMPORAL`: se conserva como estado heredado, con cinco juegos secuenciales, hasta que Equipo 0 confirme su conversión. No se trata como Plus/Pro por su nombre ni se le asigna una regla nueva.
- Se conserva el límite de cinco intentos por juego y ciclo diario en el endpoint de envío.
- El historial de ciclos anteriores no se elimina; al cambiar la fecha local se crea un ciclo nuevo.
- `DailyExerciseProgress.ducky_coin_reward_processed` identifica el procesamiento de la recompensa de moneda por juego/ciclo. El evento externo no se simula.

## Límites conocidos / integración pendiente

- El nivel de acceso se captura en `DailyCycle` al crearlo. El cambio de membresía durante el mismo día requiere el contrato de Equipo 0/Ecomotor para aplicar el orden acordado de notificación, actualización de XP y habilitación de acceso. No se ha inventado un evento de integración.
- Los importes acordados siguen siendo: 2 XP por juego completado para Free y 5 XP para Plus/Pro; una Duki Coin por la primera finalización diaria de cada juego distinto. El envío de esos eventos queda pendiente de los contratos reales de Ecomotor y Duki Bank/Equipo 5.
- La selección aleatoria se protege con transacción y bloqueo de fila donde el motor de base de datos lo soporta. SQLite no garantiza el mismo comportamiento de concurrencia que PostgreSQL; la concurrencia debe comprobarse en el motor de despliegue definitivo.
- Si hay menos de tres juegos activos entre 1–6, se seleccionan los disponibles. En la carga normal deben existir los seis primeros juegos.
- El contenido educativo sigue pendiente por decisión del equipo; un juego disponible en F6 no implica que tenga una variante publicada y pueda validarse.

## Validación local pendiente

Desde `DuckyTraining/backend`, con el entorno virtual del proyecto activado:

```powershell
py -3.15 manage.py makemigrations --check --dry-run
py -3.15 manage.py check
py -3.15 manage.py migrate
py -3.15 manage.py test apps.training
```

No se ejecutaron comandos de Django durante la preparación de este ZIP.
