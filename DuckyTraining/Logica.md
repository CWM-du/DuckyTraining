# Lógica funcional · Equipo 3 · DuckyTraining

## Estado del documento

- Estado: reglas de acceso y progreso implementadas en entorno provisional; contenido
  educativo y contratos de Rewards/Duki Bank pendientes.
- Alcance: Equipo 3 · DuckyTraining.
- No contiene código, migraciones ni datos educativos definitivos.
- Regla de prioridad: la especificación concreta de DuckyTraining prevalece ante conflictos con instrucciones generales.
- Gestión de acceso: temporalmente propia de DuckyTraining; en integración será responsabilidad compartida de los Equipos 0 y 5.

## Propósito

DuckyTraining es el módulo individual de práctica de DuckyWorld/DuckyArenas. Permite aprender mediante ejercicios breves, recibir explicaciones tras un error, ganar XP por resultados válidos y conseguir DuckyCoins al completar el cupo diario de retos disponible para el nivel de acceso del usuario.

No es un requisito para abrir QuizArenas, DuckyClash, DuckyEscape ni DuckyBank. Sus ejercicios pueden introducir mecánicas relacionadas con esos sectores, pero no bloquean ni habilitan su acceso.

## Principios funcionales

- La validación ocurre en el servidor.
- El cliente no determina si una respuesta es correcta, qué XP recibe ni si obtiene DuckyCoins.
- Las instrucciones aparecen antes de resolver cada ejercicio.
- Un fallo registra un intento, muestra una explicación y permite reintentar.
- XP prevista: 5 por juego completado para Free, Plus, Pro y Alumno Plus temporal vigente.
- No se conceden XP ni DuckyCoins reales hasta acordar los contratos de Rewards y Duki Bank con Equipo 5.
- Los juegos seleccionados están disponibles sin desbloqueo secuencial.
- Máximo de cinco intentos por juego y día.
- La fecha diaria usa `Europe/Madrid`.
- La racha depende de completar el cupo diario, no de entrar ni de realizar intentos fallidos.
- El historial educativo y el progreso por habilidad permanecen; el estado de retos se reinicia cada día.

## Niveles de acceso

Hasta que los Equipos 0 y 5 proporcionen el sistema oficial de perfil, suscripción o nivel, DuckyTraining usa un dato temporal propio y explícitamente sustituible.

| Nivel temporal | Naturaleza indicada | Ejercicios diarios accesibles | Estado |
|---|---|---:|---|
| `FREE` | Free | 3 aleatorios de los juegos 1–6 | Completar la selección diaria |
| `ALUMNO_PLUS_TEMPORAL` vigente | Alumno con Plus temporal | 10 | Completar los diez juegos |
| `PLUS` | Plus de pago | 10 | Completar los diez juegos |
| `PRO` | Pro de pago | 10 | Completar los diez juegos |

### Sustitución futura

El dato temporal no debe usarse como sistema final de suscripción. En la integración:

- Equipo 0 proporcionará identidad, autenticación y perfil del usuario.
- Equipo 5 proporcionará, si procede, economía, estado comercial o contrato relacionado con ventajas de pago.
- DuckyTraining consultará una interfaz o contrato común para obtener el nivel efectivo.
- La equivalencia temporal será: `FREE` → Free, `ALUMNO_PLUS_TEMPORAL` → Alumno con Plus temporal, `PLUS` → Plus, `PRO` → Pro.

## Ciclo por día natural

Cada día natural comienza un nuevo ciclo diario de DuckyTraining.

### Inicio y disponibilidad

- La fecha del ciclo se calcula con `Europe/Madrid`.
- Free recibe tres juegos elegidos aleatoriamente entre los números 1–6. La elección
  queda persistida hasta el siguiente ciclo local.
- Plus, Pro y Alumno Plus temporal vigente acceden a los diez juegos.
- El acceso temporal requiere una caducidad futura; al caducar se aplica Free.
- Todos los juegos incluidos en la selección diaria se pueden jugar sin desbloqueo
  secuencial.
- El reinicio diario no borra intentos históricos ni el progreso por habilidad.
- El máximo es de cinco intentos por juego y ciclo diario.

## Diez ejercicios base

Los formatos exigidos para la primera entrega se mantienen: Ordena el algoritmo, Encuentra el fallo y Conecta la red. El contenido cambia mediante variantes mensuales.

| Nº | Nombre lógico | Tipo | Dificultad | Habilidad | Relación introductoria |
|---:|---|---|---|---|---|
| 1 | Secuencia de inicio | Ordena el algoritmo | Fácil | Secuenciación | Lógica general de DuckyWorld |
| 2 | Orden de una respuesta | Ordena el algoritmo | Fácil | Secuenciación | Práctica relacionada con QuizArenas |
| 3 | El error visible | Encuentra el fallo | Fácil | Detección de errores | Práctica relacionada con DuckyClash |
| 4 | La opción correcta | Encuentra el fallo | Media | Lectura y decisión | Práctica relacionada con QuizArenas |
| 5 | Primera conexión | Conecta la red | Media | Relaciones entre componentes | Práctica relacionada con DuckyEscape |
| 6 | Ruta sin interrupciones | Conecta la red | Media | Diseño de conexiones | Práctica de infraestructura |
| 7 | Corrige antes de competir | Encuentra el fallo | Media | Validación | Práctica relacionada con DuckyClash |
| 8 | Ordena la estrategia | Ordena el algoritmo | Difícil | Planificación | Práctica relacionada con DuckyEscape |
| 9 | Red de salida | Conecta la red | Difícil | Resolución de problemas | Práctica relacionada con DuckyEscape |
| 10 | Encuentra el fallo | Encuentra el fallo | Difícil | Detección de errores | Cierre de secuencia |

Los nombres son lógicos de trabajo. Los enunciados, soluciones, explicaciones y recompensas concretas requieren validación educativa antes de convertirse en contenido definitivo.

## Variantes mensuales aleatorias

Los diez ejercicios conservan su tipo y finalidad, pero cambian sus preguntas o variantes mensualmente.

- Cada ejercicio debe disponer de varias variantes educativas compatibles con su tipo y dificultad.
- Al comienzo de un nuevo mes se selecciona de manera aleatoria una variante para cada ejercicio y usuario, salvo que el diseño final acuerde una selección global común.
- La variante seleccionada debe mantenerse estable para el usuario durante ese mes; una recarga, reintento o nueva visita no puede cambiarla.
- La variante del mes se reutiliza en los ciclos diarios de ese mes.
- Si no existen variantes suficientes, se permite reutilizar una variante previa. El sistema no puede generar ni inventar preguntas nuevas.
- La selección se guarda en servidor y nunca se determina en el navegador.

## Interacción del usuario

### 1. Entrada

El usuario autenticado entra en Training y ve:

- Su nivel de acceso vigente: Free, Alumno con Plus temporal, Plus o Pro.
- El número de retos que puede completar ese día.
- El progreso del cupo diario.
- El estado de cada ejercicio: disponible, no incluido en la selección o completado hoy.
- Su racha actual.
- Sus logros relacionados con Training.
- Su progreso por habilidad.
- Un siguiente paso claro para los juegos de la selección diaria que sigan pendientes.

### 2. Instrucciones

Antes de comenzar un ejercicio, el usuario ve:

- Objetivo del reto.
- Forma de interacción o envío.
- Cómo se valida la respuesta.
- Qué sucede si falla.
- Que se prevén 5 XP por juego completado y que la concesión real está pendiente.
- Qué falta para completar la selección diaria. No se presenta un saldo de DukiCoins.

La solución correcta no se muestra antes de validar la respuesta.

### 3. Resolución

El usuario resuelve uno de los formatos permitidos:

- **Ordena el algoritmo:** coloca bloques o pasos en una secuencia correcta.
- **Encuentra el fallo:** identifica un error en código, configuración o razonamiento.
- **Conecta la red:** une componentes respetando reglas sencillas.

El usuario envía su solución mediante una acción explícita. El servidor recibe solo la respuesta del usuario, recupera la variante asignada y calcula el resultado.

### 4. Feedback

Si falla:

- Se registra el intento diario y en el historial general.
- Se muestra la explicación de error configurada para la variante.
- El ejercicio sigue disponible para reintentar.
- No se concede XP real.

Si acierta por primera vez ese día:

- Se registra el ejercicio como completado para la fecha actual.
- Se actualiza el historial y el progreso por habilidad.
- El progreso por habilidad aumenta una sola vez por juego y ciclo diario.
- Si se completa toda la selección diaria, se actualiza la racha una sola vez.

Si vuelve a acertar un ejercicio ya completado ese día:

- Puede registrarse el intento conforme a la decisión de historial.
- No vuelve a incrementar el progreso por habilidad de ese juego y ciclo.
- No vuelve a procesar la finalización diaria ni la racha.

## XP y DuckyCoins

### XP

La regla prevista es 5 XP por juego completado para los cuatro niveles de acceso. La
concesión real está desactivada hasta acordar el contrato de Rewards con Equipo 5.

### DuckyCoins

La validación/evaluación inicial de Rewards, su persistencia y servicio de
procesamiento, y Duki Bank/cartera de monedas quedan **pendientes de implementar el
jueves 22**. DuckyTraining no actualiza directamente la cartera ni el saldo.

### Identificadores únicos de recompensa

Todo evento de recompensa debe incluir, como mínimo:

- Usuario.
- Fecha del ciclo en la zona horaria oficial.
- Identificador estable del ejercicio, para la XP.
- Tipo de recompensa: `TRAINING_EXERCISE_XP` o `TRAINING_DAILY_COMPLETION`.
- Nivel efectivo aplicado al ciclo, para la recompensa final.
- Resultado validado y fecha/hora.

Estos datos permiten que Equipo 5 impida duplicados por reenvíos, recargas, concurrencia o repeticiones.

## Rachas y logros

### Racha

La racha aumenta solo cuando el usuario completa el cupo íntegro de ejercicios diarios de su nivel.

| Situación | Efecto |
|---|---|
| Primera finalización diaria | Racha = 1 |
| Finalización en el día natural consecutivo | Racha +1 |
| Varias finalizaciones o reintentos el mismo día | No aumenta de nuevo |
| No completar el cupo un día | La racha se rompe al procesar la siguiente finalización o consulta de estado |
| Fallar ejercicios o abandonar la secuencia | No mantiene ni incrementa la racha |

La racha se calcula y guarda en el servidor. No se introduce por ahora multiplicador de XP, bonus automático ni penalización adicional: requerirían reglas de negocio aprobadas.

### Logros

Los logros se limitan a hitos comprobables de Training:

- Primera finalización diaria.
- Primer día consecutivo de racha.
- Hitos de racha que se definan posteriormente.
- Completar el cupo diario de cada nivel de acceso.
- Completar los diez retos diarios como usuario Pro.

Un logro se concede una sola vez cuando corresponda y debe pasar por la gestión común de progreso del Equipo 5 si ese equipo implementa logros globales.

## Relación con otros sectores

### QuizArenas

Training puede incluir ejercicios de ordenar pasos y elegir o revisar respuestas como práctica relacionada con QuizArenas. No condiciona su acceso.

### DuckyClash

Training puede incluir detección de fallos y validación de soluciones como práctica relacionada con DuckyClash. No crea duelos, no gestiona rivales y no condiciona el acceso al módulo.

### DuckyEscape

Training puede incluir secuencias y conexiones como práctica relacionada con DuckyEscape. No implementa salas, temporizador, pistas ni condiciones de Escape.

### DuckyBank y ecomotor

La integración con Rewards/Equipo 5 deberá comunicar resultados validados con un
identificador idempotente. La validación inicial de Rewards, su persistencia y
servicio de procesamiento, y Duki Bank/cartera de monedas quedan **pendientes de
implementar el jueves 22**. El entorno actual no concede XP ni DukiCoins reales.

## Datos funcionales necesarios

Los modelos provisionales representan:

- Nivel temporal de acceso del usuario y caducidad de Alumno Plus temporal.
- Ciclo diario por usuario y fecha.
- Progreso diario por ejercicio y fecha.
- Variante mensual asignada por usuario, mes y ejercicio.
- Indicadores independientes de procesamiento de XP y Duki Coins, pendientes del contrato.
- Racha: contador y última fecha de finalización.
- Logros de Training ya otorgados.
- Historial permanente de intentos y progreso por habilidad.

## Gestión de cambios de nivel durante el día

El nivel efectivo queda guardado en el ciclo diario. Si Alumno Plus temporal caduca,
se aplica Free en las siguientes consultas del mismo día y se fija una selección
Free. La sincronización con la fuente oficial de membresía sigue pendiente.

## Límites y no incluidos

Siguen pendientes:

- Contratos reales de identidad/acceso, Rewards y Duki Bank.
- Enunciados, soluciones, explicaciones y variantes educativas definitivas.
- Concesiones reales de XP y monedas.
- Logros y multiplicadores de racha.
- Nuevos minijuegos fuera de los tres formatos establecidos.
- Especializaciones, árbol de habilidades o contenidos de pago adicionales.
- Desbloqueo de otros sectores mediante Training.

## Decisiones pendientes antes de implementar

1. Acordar con Equipo 5 los contratos de Rewards y Duki Bank antes de conceder
   recompensas reales.
2. Validar enunciados, variantes, soluciones y explicaciones educativas de los diez
   ejercicios.
3. Completar la integración de identidad y acceso temporal con los equipos responsables.
4. Definir hitos de logro sin introducir recompensas no aprobadas.
