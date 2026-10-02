# Lógica funcional · Equipo 3 · DuckyTraining

## Estado del documento

- Estado: definición funcional consolidada, pendiente de implementación.
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
- Las recompensas solo pueden concederse una vez por ejercicio completado y día natural.
- Las DuckyCoins se conceden una vez al día al completar el cupo de retos del nivel del usuario.
- Los ejercicios diarios son secuenciales: para acceder al siguiente debe completarse el anterior dentro del ciclo de ese día.
- La racha depende de completar el cupo diario, no de entrar ni de realizar intentos fallidos.
- El historial educativo y el progreso por habilidad permanecen; el estado de retos se reinicia cada día.

## Niveles de acceso

Hasta que los Equipos 0 y 5 proporcionen el sistema oficial de perfil, suscripción o nivel, DuckyTraining usa un dato temporal propio y explícitamente sustituible.

| Nivel temporal | Naturaleza indicada | Ejercicios diarios accesibles | Condición de recompensa final |
|---|---|---:|---|
| `FREE` | Free | 3 | Completar ejercicios 1 a 3 del día |
| `ALUMNO_PLUS_TEMPORAL` | Alumno con Plus temporal | 5 | Completar ejercicios 1 a 5 del día |
| `PLUS` | Plus de pago | 7 | Completar ejercicios 1 a 7 del día |
| `PRO` | Pro de pago | 10 | Completar ejercicios 1 a 10 del día |

### Sustitución futura

El dato temporal no debe usarse como sistema final de suscripción. En la integración:

- Equipo 0 proporcionará identidad, autenticación y perfil del usuario.
- Equipo 5 proporcionará, si procede, economía, estado comercial o contrato relacionado con ventajas de pago.
- DuckyTraining consultará una interfaz o contrato común para obtener el nivel efectivo.
- La equivalencia temporal será: `FREE` → Free, `ALUMNO_PLUS_TEMPORAL` → Alumno con Plus temporal, `PLUS` → Plus, `PRO` → Pro.

## Ciclo por día natural

Cada día natural comienza un nuevo ciclo diario de DuckyTraining.

### Inicio del ciclo

- Los diez ejercicios son visibles todos los días.
- El ejercicio 1 está disponible al comenzar el ciclo.
- Los demás ejercicios se muestran como bloqueados por secuencia o no accesibles por límite de nivel.
- El número de ejercicios que forman parte del ciclo depende del nivel de acceso efectivo del usuario.
- El reinicio se rige por la zona horaria oficial que establezca el Equipo 0.

### Secuencia

| Nivel | Secuencia diaria necesaria |
|---|---|
| Free | 1 → 2 → 3 |
| Alumno con Plus temporal | 1 → 2 → 3 → 4 → 5 |
| Plus | 1 → 2 → 3 → 4 → 5 → 6 → 7 |
| Pro | 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 10 |

Un ejercicio puede estar visible sin estar disponible:

- **Bloqueado por secuencia:** falta completar correctamente el ejercicio anterior en el ciclo diario actual.
- **No accesible por nivel:** queda por encima del cupo del nivel del usuario.
- **Disponible:** está dentro del cupo y el anterior ya se completó, o es el ejercicio 1.
- **Completado hoy:** fue resuelto correctamente durante el ciclo actual.

A las 00:00 se reinicia la secuencia diaria. Esto no borra el historial total de intentos, XP concedida, rachas, logros ni progreso por habilidad.

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
| 10 | Reto de preparación DuckyWorld | Formato por confirmar | Difícil | Integración de habilidad | Cierre de secuencia Pro |

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
- El progreso de la secuencia diaria.
- El estado de cada ejercicio: disponible, bloqueado por secuencia, no accesible por nivel o completado hoy.
- Su racha actual.
- Sus logros relacionados con Training.
- Su progreso por habilidad.
- Un siguiente paso claro, por ejemplo: “Completa el ejercicio 2 para continuar”.

### 2. Instrucciones

Antes de comenzar un ejercicio, el usuario ve:

- Objetivo del reto.
- Forma de interacción o envío.
- Cómo se valida la respuesta.
- Qué sucede si falla.
- Que la XP se concede una vez al día por ese ejercicio completado.
- Qué falta para completar el cupo diario y optar a DuckyCoins.

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
- No se concede XP ni se desbloquea el siguiente ejercicio.

Si acierta por primera vez ese día:

- Se registra el ejercicio como completado para la fecha actual.
- Se actualiza el historial y el progreso por habilidad.
- Se solicita la XP mediante el servicio común de recompensas del Equipo 5.
- Se desbloquea el siguiente ejercicio si forma parte del cupo del usuario.
- Si se completa el último ejercicio del cupo, se procesa la finalización diaria.

Si vuelve a acertar un ejercicio ya completado ese día:

- Puede registrarse el intento conforme a la decisión de historial.
- No recibe XP adicional por ese ejercicio y día.
- No altera la finalización ya concedida ni la racha.

## XP y DuckyCoins

### XP

La XP se concede por la primera resolución correcta de cada ejercicio en cada día natural. El importe exacto por ejercicio debe definirse con el contenido educativo y el Equipo 5.

### DuckyCoins

DuckyCoins se conceden una única vez al completar todos los ejercicios diarios disponibles según el nivel actual:

- Free: después de completar 3.
- Alumno con Plus temporal: después de completar 5.
- Plus: después de completar 7.
- Pro: después de completar 10.

DuckyTraining no actualiza directamente la cartera ni el saldo. Envía el evento validado al servicio del Equipo 5.

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

Training comunica resultados validados al servicio de recompensas. Debe aportar como mínimo identificador de actividad, usuario, tipo de juego, resultado validado, fecha/hora y datos de recompensa. El Equipo 5 devuelve XP, DuckyCoins, evolución o logro si corresponde, y una indicación de duplicado.

## Datos funcionales necesarios

Además de los datos generales de ejercicios, el futuro modelo debe poder representar:

- Nivel temporal de acceso del usuario, identificable como `TEMP_REPLACE` hasta la integración con Equipos 0 y 5.
- Ciclo diario por usuario y fecha.
- Progreso diario por ejercicio y fecha.
- Variante mensual asignada por usuario, mes y ejercicio.
- Recompensa XP procesada por ejercicio y día.
- Recompensa final de DuckyCoins procesada por ciclo y día.
- Racha: contador y última fecha de finalización.
- Logros de Training ya otorgados.
- Historial permanente de intentos y progreso por habilidad.

## Gestión de cambios de nivel durante el día

No se debe implementar una regla improvisada para cambios de nivel dentro de un ciclo abierto. La regla pendiente es:

- Determinar si el cupo se fija al abrir el primer ejercicio del día o se recalcula al cambiar el nivel.
- Evitar que un cambio de nivel permita cobrar dos recompensas finales en la misma fecha.
- Si un usuario pasa temporalmente de Free a Alumno con Plus temporal, definir si puede continuar del ejercicio 4 al 5 durante ese mismo ciclo o si el cambio aplica al día siguiente.

Hasta que exista una decisión oficial, la alternativa segura para implementación será fijar el nivel efectivo al crear el ciclo diario y usarlo durante todo ese día.

## Límites y no incluidos

Este documento no autoriza todavía:

- Código, migraciones o endpoints.
- Simulación final de los contratos de Equipo 0 o Equipo 5.
- Enunciados, soluciones y explicaciones definitivas.
- Valores numéricos de XP o DuckyCoins.
- Multiplicadores de racha.
- Nuevos minijuegos fuera de los tres formatos establecidos.
- Especializaciones, árbol de habilidades o contenidos de pago adicionales.
- Desbloqueo de otros sectores mediante Training.

## Decisiones pendientes antes de implementar

1. Confirmar la zona horaria que usará el ciclo diario; provisionalmente debe ser la configuración global del Equipo 0.
2. Confirmar si el nivel efectivo se fija al inicio del ciclo diario, opción recomendada para evitar doble recompensa.
3. Definir importes de XP por ejercicio y DuckyCoins por finalización diaria con el Equipo 5.
4. Validar enunciados, variantes, soluciones y explicaciones educativas de los diez ejercicios.
5. Definir el formato del ejercicio 10, manteniéndolo dentro de Ordena el algoritmo, Encuentra el fallo o Conecta la red, salvo autorización explícita de un formato adicional.
6. Definir los hitos concretos de logro y racha, sin introducir recompensas no aprobadas.
7. Confirmar cómo se registrará el historial de intentos repetidos tras un ejercicio ya completado en el mismo día.
