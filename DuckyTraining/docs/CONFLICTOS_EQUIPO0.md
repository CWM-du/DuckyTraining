# Conflictos y decisiones con Equipo 0 · DuckyTraining

## Estado

Revisado el 2026-10-07 con las decisiones funcionales proporcionadas por Equipo 3.

## Decisiones cerradas

### Identidad y autenticación

La identidad/autenticación definitiva se aplicará posteriormente. Durante desarrollo DuckyTraining utiliza un usuario Django temporal y un perfil temporal de Training. El perfil será sustituido por el contrato oficial de Equipo 0.

### Perfil oficial

El perfil deberá poder consultar la experiencia/XP, nivel general y resumen de Duki Coins. La experiencia y el nivel general los gestiona el Ecomotor; la wallet y el historial monetario pertenecen a Duki Bank.

### Membresía

La clasificación de acceso de Training queda simplificada a:

- `FREE`: sin membresía.
- `PLUS`: con membresía.
- `PRO`: con membresía.

No se mantiene `ALUMNO_PLUS_TEMPORAL` como nivel funcional de acceso.

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

Cada partida completada puede conceder XP, incluso si es una repetición del mismo juego durante el día. La propuesta inicial es de 2–5 XP según juego y resultado. El importe definitivo pertenece al contrato del Ecomotor/Equipo 5.

### Duki Coins

La primera partida completada de cada juego durante el día concede 1 Duki Coin. Repeticiones del mismo juego conceden XP, pero no otra moneda. Otro juego distinto puede conceder su propia moneda diaria.

Duki Training no actualiza directamente la wallet.

### Acceso diario

- FREE: selección diaria de 3 juegos, renovada al día siguiente. Los juegos seleccionados se pueden repetir.
- PLUS/PRO: acceso al catálogo completo.

La selección se almacena en servidor.

## Pendientes reales

- Contrato técnico definitivo de Equipo 0 para identidad/perfil.
- Contrato de Ecomotor/Equipo 5 para XP y nivel.
- Contrato de Duki Bank/Equipo 5 para Duki Coins.
- Hitos concretos de racha/logros.
- Contenido educativo y variantes definitivas.
