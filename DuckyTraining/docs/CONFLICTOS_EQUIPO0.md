# Conflictos y decisiones con Equipo 0 · DuckyTraining

## Estado

Actualizado el 2026-10-20 con las decisiones funcionales proporcionadas por Equipo 3.

## Decisiones cerradas

### Identidad y autenticación

La identidad/autenticación definitiva se aplicará posteriormente. Durante desarrollo DuckyTraining utiliza un usuario Django temporal y un perfil temporal de Training. El perfil será sustituido por el contrato oficial de Equipo 0.

### Perfil oficial

El perfil deberá poder consultar la experiencia/XP, nivel general y resumen de Duki Coins. La experiencia y el nivel general los gestiona el Ecomotor; la wallet y el historial monetario pertenecen a Duki Bank.

### Membresía

El perfil/contrato oficial de Equipo 0 sigue pendiente. En el entorno provisional,
Training soporta estos estados:

- `FREE`: sin membresía.
- `PLUS`: con membresía.
- `PRO`: con membresía.
- `ALUMNO_PLUS_TEMPORAL`: acceso Plus hasta su fecha de caducidad.

### Zona horaria

La zona horaria oficial para el ciclo diario es **Madrid / `Europe/Madrid`**.

### Cambio de nivel

El nivel general procede del Ecomotor y depende del progreso/XP. Cuando cambia:

1. Ecomotor actualiza XP/nivel.
2. El usuario recibe la notificación.
3. Training consulta el estado actualizado.
4. Solo entonces habilita una nueva partida dependiente del nuevo estado.

La membresía y el nivel general son conceptos distintos.

## Decisiones de producto cerradas

### XP

La regla actual es de **5 XP por juego completado** para Free, Plus, Pro y Alumno
Plus temporal vigente. La concesión real está desactivada hasta acordar los contratos
de Rewards con Equipo 5; no se simulan concesiones.

### Duki Coins

La primera partida completada de cada juego durante el día concede 1 Duki Coin. Repeticiones del mismo juego conceden XP, pero no otra moneda. Otro juego distinto puede conceder su propia moneda diaria.

Duki Training no actualiza directamente la wallet. Rewards (validación/evaluación
inicial y persistencia/servicio de procesamiento) y Duki Bank/cartera de monedas
quedan **pendientes de implementar el jueves 22**.

### Acceso diario

- FREE: selección diaria aleatoria de 3 juegos entre los números 1–6.
- PLUS/PRO y Alumno Plus temporal vigente: acceso a los diez juegos.
- Máximo de 5 intentos por juego y día.

La selección se almacena en servidor.

## Pendientes reales

- Contrato técnico definitivo de Equipo 0 para identidad/perfil.
- Contrato de Ecomotor/Equipo 5 para XP y nivel.
- Contrato de Duki Bank/Equipo 5 para Duki Coins.
- Hitos concretos de racha/logros.
- Contenido educativo y variantes definitivas.
