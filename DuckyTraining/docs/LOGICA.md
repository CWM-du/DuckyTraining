# Lógica funcional · Equipo 3 · DuckyTraining

## Estado del documento

- Estado: definición funcional actualizada tras la revisión de `DAR.zip` y las decisiones posteriores de Equipo 3.
- Alcance: Equipo 3 · DuckyTraining.
- La identidad/autenticación definitiva se integrará posteriormente mediante Equipo 0; durante desarrollo se usa un entorno/configuración temporal sustituible.
- XP y niveles generales los gestiona el Ecomotor. Duki Bank gestiona la wallet y el historial de Duki Coins.
- DuckyTraining no mantiene una wallet propia ni decide el nivel general del usuario.

## Propósito

DuckyTraining es el módulo individual de práctica. Permite realizar partidas breves, recibir explicación tras un error, acumular XP y obtener Duki Coins según las reglas diarias del juego.

No es requisito para abrir otros sectores de DuckyWorld. Las referencias a otros sectores son educativas y no crean bloqueos de acceso entre módulos.

## Principios funcionales

- La validación de la respuesta ocurre en el servidor.
- El cliente no determina si una respuesta es correcta ni qué recompensa corresponde.
- Las instrucciones aparecen antes de cada partida.
- Un fallo registra un intento, muestra la explicación configurada y permite repetir.
- Cada partida correcta puede conceder XP según el resultado y el juego; la cantidad definitiva la determina el contrato del Ecomotor.
- La primera partida completada de cada juego durante el día puede conceder 1 Duki Coin.
- Repetir el mismo juego el mismo día sigue pudiendo conceder XP, pero no otra Duki Coin por ese juego.
- DukiTraining no actualiza directamente la wallet: la recompensa de Duki Coins se registra mediante la integración con Duki Bank/Equipo 5 cuando exista el contrato oficial.
- La XP y el nivel general se gestionan mediante el Ecomotor y se consultan en el perfil del usuario.
- Los cambios de nivel se aplican siguiendo la lógica del Ecomotor: el usuario recibe la notificación correspondiente, se actualiza la XP/nivel y solo después se habilita una nueva partida que dependa del nuevo estado.
- El historial de intentos y el progreso educativo permanecen entre ciclos diarios.

## Identidad, perfil y acceso

Durante desarrollo, DuckyTraining usa una representación temporal de membresía en `UserTrainingProfile`. No es el sistema definitivo de identidad.

### Membresía efectiva

Solo existen tres estados funcionales de acceso:

| Membresía | Acceso DuckyTraining |
|---|---|
| `FREE` | Tres juegos aleatorios diarios entre los números 1–6. |
| `PLUS` | Accede a los diez juegos. |
| `PRO` | Accede a los diez juegos. |
| `ALUMNO_PLUS_TEMPORAL` vigente | Accede a los diez juegos hasta su caducidad. |

La membresía no se confunde con el **nivel general** del usuario. El nivel por XP/progreso pertenece al Ecomotor.

### Perfil

La pantalla de DuckyTraining debe mostrar, cuando el contrato de perfil esté disponible:

- experiencia/XP del usuario;
- nivel general;
- resumen de Duki Coins;
- estado de las recompensas de Training;
- juegos disponibles y su estado de acceso.

La wallet completa pertenece a Duki Bank. Duki Bank conserva total ganado histórico, total gastado, saldo disponible, devoluciones/ajustes e historial de movimientos con sus referencias de origen.

## Ciclo diario

- Zona horaria oficial: **Europe/Madrid / hora de Madrid**.
- Cada día se crea un ciclo de Training por usuario.
- La selección diaria se decide y almacena en servidor; no se calcula en React.

### Usuarios FREE

- Reciben una selección diaria aleatoria de **3 juegos entre los números 1–6**.
- Pueden repetir los juegos seleccionados durante ese día.
- Al día siguiente la selección se renueva.
- Los juegos fuera de la selección diaria se muestran como no disponibles por membresía/selección.

### Usuarios PLUS y PRO

- Tienen acceso al catálogo completo de DuckyTraining.
- No dependen de una selección diaria limitada para poder jugar.

### Alumno Plus temporal

- Tiene acceso a los diez juegos solo mientras el acceso temporal esté vigente.
- Al caducar, se aplica el acceso Free en las siguientes consultas del ciclo.

### Estados diarios

Los estados funcionales son:

- **Disponible:** el juego pertenece al catálogo accesible en el ciclo.
- **Completado hoy:** el usuario ya completó correctamente ese juego en el ciclo actual.
- **No disponible por membresía/selección:** el juego no está incluido en el acceso actual.

No existe ya el antiguo bloqueo secuencial 1→2→3→... como regla de acceso diario.

## Recompensas

### XP por partida

Cada juego completado correctamente tiene una recompensa prevista de **5 XP** para
Free, Plus, Pro y Alumno Plus temporal vigente. La concesión real sigue desactivada
hasta disponer de los contratos de Rewards y Equipo 5.

### Duki Coin por juego y día

- La regla de producto prevista es una Duki Coin por primera partida completada del
  día de cada juego, sin monedas adicionales por repetición.
- Esta regla no se procesa en el entorno provisional: no se conceden monedas ni se
  modifica una cartera local.
- La validación de Rewards, su persistencia/servicio de procesamiento y la cartera
  de Duki Bank quedan **pendientes de implementar el jueves 22**.

La wallet y el historial monetario son responsabilidad de Duki Bank.

## Cambio de nivel durante el día

El nivel general es responsabilidad del Ecomotor y depende del progreso/XP alcanzado.

Cuando una partida provoca un cambio de nivel:

1. el Ecomotor actualiza la XP y el nivel;
2. el usuario recibe la notificación correspondiente;
3. DuckyTraining consulta el estado actualizado;
4. solo después se habilita una nueva partida que dependa del nuevo nivel.

No se debe conceder dos veces la misma recompensa por un cambio de nivel.

La membresía de acceso (FREE/PLUS/PRO) es un concepto separado del nivel general.

## Ejercicios

Se mantienen los tres formatos permitidos para la primera entrega:

1. Ordena el algoritmo.
2. Encuentra el fallo.
3. Conecta la red.

El catálogo lógico mantiene los diez ejercicios definidos previamente. El formato definitivo del ejercicio 10 sigue pendiente de confirmación dentro de estos tres formatos.

## Variantes mensuales

- Las variantes se seleccionan en servidor.
- Una variante asignada a un usuario permanece estable durante el mes.
- La selección cambia al comenzar un nuevo mes.
- No se generan preguntas nuevas automáticamente si no existe una variante educativa aprobada.

## Intentos, habilidades, rachas y logros

- Cada envío debe poder registrarse como intento, correcto o incorrecto.
- El progreso por habilidad permanece de forma permanente.
- Los fallos no conceden XP ni Duki Coin.
- Los aciertos actualizan el progreso educativo una sola vez por juego y ciclo.
- La racha se procesa una vez al completar toda la selección diaria.
- Los logros de Training deben basarse en hitos verificables y no inventar recompensas económicas locales.

## Dependencias externas

### Equipo 0

Proporcionará posteriormente el contrato oficial de identidad/perfil. DuckyTraining debe consumir ese contrato y sustituir el perfil temporal.

### Ecomotor

Gestiona XP y nivel general. DuckyTraining solicita/consume el estado necesario y no mantiene un sistema paralelo de niveles.

### Duki Bank / Equipo 5

Gestiona la wallet de Duki Coins y su historial. DuckyTraining enviará el evento de recompensa cuando exista el contrato oficial y no modificará directamente el saldo.

## Decisiones cerradas en esta revisión

- Identidad/autenticación: se integra posteriormente; durante desarrollo se usa configuración temporal y sustituible.
- Membresías de acceso: Free, Plus, Pro y Alumno Plus temporal vigente.
- Free: selección diaria aleatoria de 3 juegos entre 1–6.
- Plus/Pro/Alumno Plus temporal vigente: catálogo completo de 10 juegos.
- Repetición: permitida durante el día.
- Intentos: máximo de 5 por juego y día.
- XP previsto: 5 por juego completado en los cuatro tipos de acceso; concesión real pendiente.
- Duki Coin: 1 por juego y día, solo en la primera partida completada de ese juego.
- Zona horaria: Madrid (`Europe/Madrid`).
- Nivel general: lo gestiona Ecomotor según progreso/XP.
- Cambio de nivel: se aplica después de la actualización/notificación del Ecomotor y antes de habilitar una nueva partida dependiente de ese nivel.

## Pendientes que siguen abiertos

- Contrato técnico definitivo de identidad/perfil de Equipo 0.
- Contrato definitivo de XP con Ecomotor/Equipo 5.
- Contrato definitivo de Duki Coins con Duki Bank/Equipo 5.
- Rewards: validación/evaluación inicial y persistencia/servicio de procesamiento.
- Duki Bank y cartera de monedas.
- Hitos concretos de logros.
- Enunciados, soluciones, explicaciones y variantes educativas definitivas de los diez ejercicios.
