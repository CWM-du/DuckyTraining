# Lógica funcional · Equipo 3 · DuckyTraining

## Estado del documento

- Estado: propuesta funcional pendiente de confirmación antes de implementarse.
- Alcance: Equipo 3 · DuckyTraining.
- No es código ni sustituye todavía los contratos oficiales de los Equipos 0 y 5.
- Regla de prioridad: la especificación concreta de DuckyTraining prevalece cuando entre en conflicto con directrices generales.

## Propósito de DuckyTraining

DuckyTraining es la puerta de práctica individual de DuckyWorld/DuckyArenas. Su objetivo es que cada usuario:

1. Aprenda de forma guiada y sin competición.
2. Reciba instrucciones antes de empezar y una explicación cuando falle.
3. Resuelva ejercicios progresivos para ganar XP.
4. Desbloquee el acceso progresivo a los demás sectores del proyecto.
5. Mantenga un historial de intentos y progreso por habilidad.

El entrenamiento no reemplaza QuizArenas, DuckyClash ni DuckyEscape. Prepara al alumno para interactuar con ellos con una base mínima de lógica, corrección de errores, lectura de reglas y resolución de retos.

## Principios obligatorios

- La validación de respuestas se realiza en el servidor.
- El navegador nunca decide si una respuesta es correcta, cuánta XP concede ni qué contenido queda desbloqueado.
- Las instrucciones deben ser visibles antes de comenzar cada ejercicio.
- Un fallo debe proporcionar una explicación comprensible y permitir un nuevo intento cuando corresponda.
- La recompensa base de un ejercicio no puede pagarse más de una vez.
- El sistema debe guardar intentos, primera resolución y progreso por habilidad.
- No se crea contenido competitivo dentro de DuckyTraining: el módulo es individual.
- Las reglas de desbloqueo y progreso deben mostrarse de forma clara al usuario.

## Calendario diario de diez ejercicios

La primera secuencia contiene diez ejercicios introductorios. Cada ejercicio está vinculado a un día del mes: días 1 a 10.

| Día del mes | Ejercicio | Tipo | Dificultad progresiva | Habilidad principal | Relación con DuckyWorld |
|---|---|---|---|---|---|
| 1 | Secuencia de inicio | Ordena el algoritmo | Fácil | Secuenciación | Base general de lógica para todos los sectores |
| 2 | Orden de una respuesta | Ordena el algoritmo | Fácil | Secuenciación | Introducción a responder pasos en QuizArenas |
| 3 | El error visible | Encuentra el fallo | Fácil | Detección de errores | Introducción a retos de DuckyClash |
| 4 | La opción correcta | Encuentra el fallo | Media | Lectura y decisión | Introducción a preguntas de QuizArenas |
| 5 | Primera conexión | Conecta la red | Media | Relaciones entre componentes | Introducción a DuckyEscape y retos técnicos |
| 6 | Ruta sin interrupciones | Conecta la red | Media | Diseño de conexiones | Preparación para pruebas de infraestructura |
| 7 | Corrige antes de competir | Encuentra el fallo | Media | Validación | Preparación para DuckyClash |
| 8 | Ordena la estrategia | Ordena el algoritmo | Difícil | Planificación | Preparación para cadenas de pruebas de DuckyEscape |
| 9 | Red de salida | Conecta la red | Difícil | Resolución de problemas | Preparación para una habitación de DuckyEscape |
| 10 | Reto de preparación DuckyWorld | Tipo definido por contenido | Difícil | Integración de habilidad | Cierre de iniciación y acceso progresivo a sectores |

La tabla define el contenido funcional esperado, no enunciados, soluciones ni recompensas numéricas definitivas. Estos elementos requieren validación educativa antes de cargarse como datos reales.

## Regla de disponibilidad por día

Cada ejercicio se asocia a `unlock_day`, con valores del 1 al 10.

- El ejercicio 1 se puede intentar únicamente cuando el día del mes sea 1 o posterior.
- El ejercicio 2 se puede intentar únicamente cuando el día del mes sea 2 o posterior y el ejercicio 1 esté completado.
- El ejercicio N se puede intentar únicamente cuando el día del mes sea igual o superior a N y el ejercicio N−1 esté completado.
- Si el usuario no completa el ejercicio disponible, el siguiente permanece bloqueado aunque llegue su día del mes.
- El ejercicio bloqueado debe mostrar su condición de desbloqueo, sin revelar su solución.

Ejemplo: si hoy es día 5 y el alumno ha completado los ejercicios 1, 2 y 3, pero no el 4, podrá abrir el ejercicio 4. El ejercicio 5 continuará bloqueado hasta completar el 4, aunque el calendario ya permita su fecha.

## Aclaración necesaria sobre ciclos mensuales

La frase “se desbloquean por día del mes” permite dos interpretaciones. Esta propuesta adopta la más conservadora para no castigar al alumno:

- Los ejercicios 1 a 10 se desbloquean por fecha durante el ciclo inicial.
- Tras desbloquearse, un ejercicio no vuelve a bloquearse al terminar el mes.
- Completar un ejercicio tarde no elimina la posibilidad de continuar la secuencia.
- No se implementan rachas, reinicios mensuales ni penalizaciones por ausencia, porque no forman parte de la primera entrega obligatoria.

Si se desea que los diez ejercicios se reinicien cada mes o que haya una nueva secuencia mensual, será una ampliación y necesitará reglas propias de recompensa, repetición y calendario.

## Secuencia de interacción

### 1. Entrada a Training

El usuario autenticado abre DuckyTraining desde la navegación general. Ve:

- El ejercicio actual disponible.
- Los ejercicios ya completados.
- Los ejercicios futuros bloqueados.
- La condición de fecha y requisito previo de cada bloqueo.
- Su progreso por habilidad.
- La XP obtenida en los ejercicios ya resueltos, cuando el servicio oficial de recompensas esté integrado.

La interfaz debe indicar un siguiente paso claro: “Completa el ejercicio X para desbloquear el siguiente”.

### 2. Consulta de instrucciones

Antes de empezar, el usuario accede a una pantalla de instrucciones. La pantalla explica:

- Qué debe resolver.
- Cómo enviar su respuesta.
- Qué ocurre si falla.
- Que la validación se realiza en el servidor.
- Qué progreso puede obtener al completar el ejercicio por primera vez.

No debe mostrar la respuesta correcta antes del envío.

### 3. Resolución

El usuario realiza uno de los tres formatos de ejercicio:

- **Ordena el algoritmo:** organiza bloques o pasos en una secuencia correcta.
- **Encuentra el fallo:** identifica un error en código, configuración o razonamiento.
- **Conecta la red:** une componentes respetando reglas simples de conexión.

El envío se realiza mediante una acción explícita y protegida. El servidor comprueba la solución.

### 4. Feedback

Si la respuesta es incorrecta:

- Se incrementa el historial de intentos.
- Se muestra una explicación del error acorde al ejercicio.
- Se permite volver a intentarlo.
- No se concede la recompensa base.

Si la respuesta es correcta por primera vez:

- Se marca el ejercicio como completado.
- Se registra la fecha de resolución.
- Se actualiza el progreso por habilidad.
- Se solicita al servicio del Equipo 5 la recompensa de XP y, si la regla final lo contempla, DuckyCoins.
- Se desbloquea el siguiente ejercicio si su día de calendario ya ha llegado.
- Si la finalización cumple la condición definida para acceso a otro sector, el servidor registra ese acceso.

Si el ejercicio ya estaba completado:

- Puede conservarse el registro de un nuevo intento para el historial.
- No se concede nuevamente la recompensa base.
- No se implementan recompensas por mejora hasta que exista una regla aprobada para calcularla.

## Progreso y experiencia

### XP

La XP representa el progreso educativo y no se gasta. DuckyTraining concede XP por resolver ejercicios nuevos con resultado validado.

La cantidad exacta de XP no se fija en este documento. Cada ejercicio mantiene un valor de recompensa que debe ser confirmado por el contenido educativo y aplicado exclusivamente mediante el servicio común del Equipo 5.

### DuckyCoins

DuckyCoins pueden existir como recompensa de actividad según el diseño general. DuckyTraining no modificará carteras directamente. Cuando proceda, enviará el resultado validado al servicio del Equipo 5.

### Progreso por habilidad

Cada ejercicio se clasifica con una habilidad. Para esta primera secuencia se proponen únicamente habilidades que se desprenden de los formatos obligatorios:

- Secuenciación.
- Detección de errores.
- Lectura y decisión.
- Relaciones entre componentes.
- Diseño de conexiones.
- Validación.
- Planificación.
- Resolución de problemas.
- Integración de habilidad.

El progreso por habilidad se actualiza tras cada intento y, de forma diferenciada, tras la primera resolución correcta. No se crearán rangos, especializaciones ni árboles de habilidades en esta entrega porque son ampliaciones del proyecto general.

## Relación con los demás juegos

### QuizArenas

DuckyTraining introduce la lectura de instrucciones, la toma de decisiones y el envío de una respuesta validada por servidor. Estos son aprendizajes previos para participar en cuestionarios sin exponer la lógica interna de QuizArenas.

El acceso a QuizArenas debe depender de una condición global definida por el Equipo 0 y validada por servidor. La recomendación funcional es exigir haber completado el ejercicio introductorio correspondiente, pero el identificador técnico y la regla final deben acordarse con el Equipo 0.

### DuckyClash

DuckyTraining prepara al alumno para detectar errores y justificar una solución antes de un reto amistoso. No crea duelos, no selecciona rivales y no gestiona resultados competitivos.

El acceso a DuckyClash debe requerir una condición definida con el Equipo 0. La propuesta es que el usuario complete el ejercicio introductorio de detección de errores asignado a DuckyClash.

### DuckyEscape

DuckyTraining prepara cadenas de razonamiento, orden de acciones y conexiones simples. DuckyEscape conserva su propia historia, salas, temporizador y reglas de pistas.

El acceso a DuckyEscape debe depender de una condición acordada por el Equipo 0. La propuesta es exigir la finalización de los ejercicios introductorios vinculados a secuencia y conexiones.

### DuckyBank y ecomotor

DuckyTraining comunica un resultado validado al servicio común de recompensas. Debe incluir al menos:

- Identificador único de actividad finalizada.
- Usuario que la completó.
- Tipo de juego: `DUCKY_TRAINING`.
- Resultado validado.
- Fecha y hora.
- Datos del ejercicio necesarios para determinar XP y monedas.

El Equipo 5 devuelve el resumen de XP, monedas y cualquier desbloqueo aplicable, además de indicar si el evento fue duplicado. DuckyTraining no simula ni modifica el saldo, la evolución o el inventario.

## Reglas de desbloqueo de otros sectores

El requisito de usar los diez ejercicios como primera interacción para ganar XP y avanzar hacia las demás modalidades necesita una regla explícita para no bloquear indebidamente funciones de otros equipos.

Propuesta mínima, pendiente de aprobación del Equipo 0:

| Sector | Condición propuesta | Motivo |
|---|---|---|
| DuckyTraining | Usuario autenticado | Es la ruta inicial individual |
| QuizArenas | Ejercicios 1 a 4 completados | Introducción a orden, respuesta y decisión |
| DuckyClash | Ejercicios 1 a 3 y 7 completados | Preparación para detectar y corregir fallos |
| DuckyEscape | Ejercicios 1, 5, 6, 8 y 9 completados | Preparación para secuencias, conexiones y retos encadenados |
| DuckyBank | Usuario autenticado y existencia de cartera gestionada por Equipo 5 | El acceso a cartera no debe depender de Training salvo acuerdo global |

El ejercicio 10 funciona como cierre de iniciación de DuckyWorld y evidencia que el alumno ha completado la secuencia de entrenamiento. No se asigna automáticamente una funcionalidad adicional fuera de la XP y los desbloqueos que se confirmen.

## Estados funcionales de un ejercicio

Cada ejercicio debe tener un estado visible para el usuario:

- **Bloqueado por fecha:** todavía no ha llegado el día del mes requerido.
- **Bloqueado por progreso:** ya llegó la fecha, pero falta completar el ejercicio anterior.
- **Disponible:** ha llegado la fecha y se cumplen los requisitos previos.
- **En curso:** el usuario está resolviendo el ejercicio.
- **Completado:** el ejercicio fue resuelto correctamente al menos una vez.

No se introduce un estado de fracaso permanente: el alumno puede volver a intentarlo tras un error.

## Datos necesarios por ejercicio

Además de los campos de contenido ya definidos para DuckyTraining, cada ejercicio diario necesitará conceptualmente:

- Identificador estable del ejercicio.
- Día de desbloqueo (`unlock_day`).
- Orden de la secuencia (`sequence_order`).
- Tipo de ejercicio.
- Habilidad principal.
- Instrucciones.
- Enunciado.
- Datos de interacción del formato.
- Solución almacenada solo en servidor.
- Explicación de error.
- XP y, si procede, DuckyCoins de recompensa.
- Relación de introducción con un sector de DuckyWorld, cuando aplique.

Los valores concretos de contenido y recompensa siguen pendientes de aprobación educativa y del contrato del Equipo 5.

## Límites de esta propuesta

No se incluyen todavía:

- Código.
- Migraciones.
- Datos de ejercicios finales.
- Regla de repetición mensual.
- Racha diaria.
- Penalizaciones por no entrar un día.
- Recompensas adicionales por velocidad, mejora o variantes.
- Especializaciones Developer, Ciberseguridad, AdminSys, Gamer o Data & AI.
- Implementación del bloqueo global de otros equipos.
- Servicios simulados de los Equipos 0 o 5.

## Decisiones pendientes antes de implementar

1. Confirmar que la secuencia de diez ejercicios se desbloquea una sola vez por día del mes y permanece disponible posteriormente.
2. Confirmar o modificar la tabla de acceso progresivo a QuizArenas, DuckyClash y DuckyEscape.
3. Validar los enunciados, soluciones y explicaciones educativas concretas de los diez ejercicios.
4. Definir las recompensas de XP y DuckyCoins por ejercicio con el Equipo 5.
5. Acordar con el Equipo 0 dónde se registra y consulta el permiso de acceso a cada sector.
6. Definir si los días 11 a 31 no tendrán ejercicios en la primera entrega o si existirán contenidos posteriores.
7. Confirmar si el ejercicio 10 será únicamente un cierre de iniciación o desbloqueará un hito adicional documentado.
