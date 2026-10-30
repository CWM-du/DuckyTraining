# Comparación de proyectos y registro de cambios

## Identificación de las entradas

- **Proyecto remoto de referencia:** `DuckyTraining-feature_hugo(4).zip`. Contenía `.git`, la rama `feature_hugo`, un historial de commits que incluye la conexión JWT y la fase 7, además de artefactos locales que se excluyeron del paquete de entrega.
- **Revisión anterior:** `DuckyTraining-feature_hugo(3).zip`. No contenía `.git`; su árbol de fuentes coincide con la revisión provisional anterior.

Se compararon los archivos bajo `DuckyTraining/`, excluyendo de la comparación los entornos virtuales, `node_modules`, `dist`, `__pycache__` y otros artefactos generados. La revisión anterior contenía 73 archivos de proyecto relevantes y el remoto 74 (la diferencia de conteo era la base SQLite local, excluida del ZIP final). Se identificaron 20 archivos de fuente/documentación con diferencias entre ambas entradas.

## Cambios útiles del remoto conservados

- Flujo de autenticación SimpleJWT y servicios frontend (`App.jsx`, `authApi.js`, `trainingApi.js`).
- Rutas existentes de overview, envío de respuestas, progreso e historial.
- Implementación de ciclo diario, selección Free persistida, límite de intentos, progreso por habilidad y racha.
- Modelos existentes y cadena de migraciones 0001–0009, incluyendo la restauración de `access_level`, el estado separado de XP/moneda, la caducidad temporal y la definición del juego 10.
- Estructura existente de los tres tipos de juego y sus componentes React.
- Configuración `Europe/Madrid` y `USE_TZ = True` ya presentes en settings.
- Contrato del historial/progreso y el enfoque de no conceder XP/monedas reales sin integración acordada.

## Cambios aplicados en esta entrega

- Sustituido el JSON de catálogo inconsistente por diez variantes técnicas completas, una por juego, todas marcadas `provisional`, con versión, enunciado, instrucciones, datos de entrada, reglas de validación y explicaciones.
- Ampliada la validación del catálogo para rechazar contenido incompleto o mal formado antes de usarlo.
- El cargador y las vistas solo habilitan variantes `published`; las variantes provisionales se conservan para revisión y no se sirven ni validan como ejercicios jugables.
- Añadida etiqueta visible de contenido provisional en el frontend.
- Añadido JSON de configuración provisional y cargador con validación estricta. La configuración Django ahora lee clave, DEBUG y hosts desde variables de entorno con valores locales inseguros explícitos como fallback.
- Añadidos adaptadores sustituibles de membresía y preparación de eventos de recompensas con claves deterministas. No existe concesión real ni cartera local.
- Actualizadas pruebas existentes para reflejar que hay contenido provisional utilizable, manteniendo explícita la separación entre contenido provisional y aprobado.
- Actualizados README y TODO, y añadido este informe comparativo.

## Diferencias y riesgos observados

- La revisión anterior y el remoto tenían divergencias en README, catálogo, migraciones 0004–0009, tests, vistas, documentación de fases y varios componentes/servicios del frontend. Se conservaron los cambios del remoto como base; no se sobrescribió el proyecto con la revisión anterior.
- El historial de migraciones contiene dos ramas históricas `0002_*` unidas por `0004_merge_20261013_1101`. La cadena posterior restaura los nombres/campos que coinciden con los modelos actuales. No se reescribieron migraciones históricas ni se añadió una migración correctiva sin evidencia estática de que faltara un campo.
- La revisión estática no puede demostrar que el esquema real de una base de datos existente esté actualizado. Debe ejecutarse `makemigrations --check --dry-run` y `migrate` localmente.
- El perfil de membresía sigue siendo una fuente local provisional. También existe el modelo heredado `apps.users.ProfileUserTraining`; no se ha eliminado ni elevado a fuente oficial y requiere decisión de Equipo 0/Core. El adaptador no representa identidad oficial de Equipo 0/Core.
- Las intenciones de XP/moneda son metadatos candidatos en la respuesta, no un outbox persistente. El procesamiento y la confirmación dependen de contratos pendientes con Equipo 5.
- El contenido temporal está diseñado para probar formatos y validación, no para enseñar conceptos como contenido curricular definitivo.
- No se ejecutaron Django, migraciones, tests ni build de React. El ZIP final excluye `.git`, `.venv`, `node_modules`, `dist` y base de datos local.

## Comandos de validación local pendientes

Desde `DuckyTraining/backend`:

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py migrate
python manage.py test apps.training
```

Desde `DuckyTraining/frontend`:

```bash
npm install
npm run build
```

`npm install` puede requerir acceso al registro de paquetes.

## Revisión de los JSON educativos recibidos

Se revisaron los archivos de origen ubicados bajo `backend/apps/training/content/`:

- `../backend/apps/training/content/asociar_conceptos (1).json`: 100 pruebas en cinco niveles, con 20 pruebas por nivel.
- `../backend/apps/training/content/detectar_error.json`: 100 pruebas en cinco niveles, con 20 pruebas por nivel.
- `../backend/apps/training/content/ordenar_codigo (1).json`: 100 pruebas en cinco niveles, con 20 pruebas por nivel.

La comprobación estática confirmó que los tres archivos se analizan como JSON, sus identificadores de prueba no se repiten dentro de cada archivo ni entre los 300 registros, las asociaciones apuntan a conceptos y explicaciones existentes sin repetir parejas de respuesta, cada prueba de detección tiene exactamente una línea marcada con error y cada orden correcto contiene los identificadores de sus bloques una sola vez. No se encontró una asignación de esos registros a números de juego ni metadatos de aprobación editorial. Por decisión del usuario, se pueden jugar desde un área de práctica separada; siguen provisionales y no se integran en `catalog.json`.

| Dataset recibido | Tipo declarado | IDs / cantidad verificados | Versión declarada | Origen de aprobación | Estado / disponibilidad |
|---|---|---|---|---|---|
| `content/asociar_conceptos (1).json` | `asociar_conceptos` | `ASO-1-01`–`ASO-5-20`; 100 | No declarada | No proporcionado | Provisional; disponible solo en el área de práctica independiente |
| `content/ordenar_codigo (1).json` | `ordenar_codigo` | `ORD-1-01`–`ORD-5-20`; 100 | No declarada | No proporcionado | Provisional; disponible solo en el área de práctica, sin número de juego asignado |
| `content/detectar_error.json` | `detectar_error` | `ERR-1-01`–`ERR-5-20`; 100 | No declarada | No proporcionado | Provisional; disponible solo en el área de práctica, sin número de juego asignado |

El catálogo real contiene diez juegos: `ORDER_ALGORITHM` en 1, 2 y 8; `FIND_ERROR` en 3, 4, 7 y 10; y `CONNECT_NETWORK` en 5, 6 y 9. El comando `seed_logical_exercises.py` y `catalog.json` respaldan estas asignaciones de tipo, pero no asignan los ejercicios `ORD-*` o `ERR-*` a esos números. Por tanto, solo puede afirmarse que esos son números candidatos por compatibilidad técnica; el mapeo de contenido permanece sin confirmar.

El identificador `asociar_conceptos` no figura como tipo soportado en `ExerciseType` y no se integra en los juegos numerados. Para permitir la solicitud de práctica, se añadió una validación de servidor aislada en `provided_games.py` y una interfaz independiente; esto no modifica el catálogo diario ni constituye aprobación para una integración oficial. En este modo, la respuesta contiene la lista completa de parejas por texto y se valida como coincidencia exacta; no se implementa puntuación parcial.

`CONNECT_NETWORK` sí está implementado de extremo a extremo. Su contenido requiere `nodes` con `id` y `label`, y `expected_connections` con pares de nodos válidos; el cliente envía `connections` y el backend valida la igualdad de las conexiones no dirigidas. La vista solo registra intentos tras encontrar una variante utilizable. Sin embargo, las variantes actuales son demos provisionales y no hay contenido aprobado recibido.

Para el ciclo diario, el cargador devuelve solo variantes con `status: "published"`; una asignación antigua a una variante provisional o una clave que ya no existe en el catálogo se considera pendiente. No se reasigna ni borra automáticamente esa asignación. El overview expone `CONTENT_PENDING` y el envío responde `409 educational_content_pending` cuando no hay contenido publicado. Las diez variantes actuales siguen provisionales. La nueva área de práctica es una excepción explícita solicitada por el usuario: sirve los tres JSON bajo una API separada, los marca provisionales, valida en servidor, revela la solución solo tras el envío y no registra intentos, puntuación ni progreso diario.

## Inventario de juegos y contenido actual

Los nombres, números, tipos, habilidades y relaciones de la tabla proceden del comando `seed_logical_exercises.py`; las claves, versiones y estados proceden de `content/catalog.json`. El origen editorial o la evidencia de aprobación no está registrado para las demos. Los datasets fuente se leen mediante la API de práctica independiente, pero no son cargados por el catálogo del ciclo diario.

| Juego | Tipo técnico verificado | Ejercicio del catálogo | Variante / versión | Estado / disponibilidad | Origen registrado | Decisión pendiente |
|---:|---|---|---|---|---|---|
| 1 | `ORDER_ALGORITHM` | Secuencia de inicio · Secuenciación | `ex01_temp_v1` / `ducky-temp-v1` | `provisional` / no ejecutable | Demo técnica en `backend/apps/training/content/catalog.json`; no se identifica autoría o aprobación | Aprobar y asignar contenido concreto, o sustituir demo; no asignar `ORD-*` sin acta/fuente |
| 2 | `ORDER_ALGORITHM` | Orden de una respuesta · Secuenciación | `ex02_temp_v1` / `ducky-temp-v1` | `provisional` / no ejecutable | Demo técnica en `backend/apps/training/content/catalog.json`; no se identifica autoría o aprobación | Aprobar y asignar contenido concreto, o sustituir demo; no asignar `ORD-*` sin acta/fuente |
| 3 | `FIND_ERROR` | El error visible · Detección de errores | `ex03_temp_v1` / `ducky-temp-v1` | `provisional` / no ejecutable | Demo técnica en `backend/apps/training/content/catalog.json`; no se identifica autoría o aprobación | Aprobar y asignar contenido concreto, o sustituir demo; no asignar `ERR-*` sin acta/fuente |
| 4 | `FIND_ERROR` | La opción correcta · Lectura y decisión | `ex04_temp_v1` / `ducky-temp-v1` | `provisional` / no ejecutable | Demo técnica en `backend/apps/training/content/catalog.json`; no se identifica autoría o aprobación | Aprobar y asignar contenido concreto, o sustituir demo; no asignar `ERR-*` sin acta/fuente |
| 5 | `CONNECT_NETWORK` | Primera conexión · Relaciones entre componentes | `ex05_temp_v1` / `ducky-temp-v1` | `provisional` / no ejecutable | Demo técnica en `backend/apps/training/content/catalog.json`; no hay dataset aprobado recibido | Reemplazar por ejercicio completo aprobado; no inventar nodos, conexiones ni explicaciones |
| 6 | `CONNECT_NETWORK` | Ruta sin interrupciones · Diseño de conexiones | `ex06_temp_v1` / `ducky-temp-v1` | `provisional` / no ejecutable | Demo técnica en `backend/apps/training/content/catalog.json`; no hay dataset aprobado recibido | Reemplazar por ejercicio completo aprobado; no inventar nodos, conexiones ni explicaciones |
| 7 | `FIND_ERROR` | Corrige antes de competir · Validación | `ex07_temp_v1` / `ducky-temp-v1` | `provisional` / no ejecutable | Demo técnica en `backend/apps/training/content/catalog.json`; no se identifica autoría o aprobación | Aprobar y asignar contenido concreto, o sustituir demo; no asignar `ERR-*` sin acta/fuente |
| 8 | `ORDER_ALGORITHM` | Ordena la estrategia · Planificación | `ex08_temp_v1` / `ducky-temp-v1` | `provisional` / no ejecutable | Demo técnica en `backend/apps/training/content/catalog.json`; no se identifica autoría o aprobación | Aprobar y asignar contenido concreto, o sustituir demo; no asignar `ORD-*` sin acta/fuente |
| 9 | `CONNECT_NETWORK` | Red de salida · Resolución de problemas | `ex09_temp_v1` / `ducky-temp-v1` | `provisional` / no ejecutable | Demo técnica en `backend/apps/training/content/catalog.json`; no hay dataset aprobado recibido | Reemplazar por ejercicio completo aprobado; no inventar nodos, conexiones ni explicaciones |
| 10 | `FIND_ERROR` | Encuentra el fallo · Detección de errores | `ex10_temp_v1` / `ducky-temp-v1` | `provisional` / no ejecutable | Demo técnica en `backend/apps/training/content/catalog.json`; no se identifica autoría o aprobación | Aprobar y asignar contenido concreto, o sustituir demo; no asignar `ERR-*` sin acta/fuente |

El estado `published` es el selector de ejecución del catálogo diario, pero no constituye evidencia editorial por sí solo. Antes de cambiarlo se requiere aprobación trazable y registro de su fuente; el contenido de demostración no debe publicarse mediante un cambio de estado solamente. La práctica separada permanece `provisional` explícitamente y no crea intentos ni progreso.

## Matriz de mapeo sin confirmar

| Categoría recibida | Números candidatos por formato | Evidencia del código | Confianza técnica | Estado del mapeo de contenido |
|---|---|---|---|---|
| Ordenar (`ORD-*`) | 1, 2, 8 | `seed_logical_exercises.py`; `catalog.json`; contrato `ORDER_ALGORITHM` | Alta para compatibilidad del tipo | Sin confirmar: falta asignar los ejercicios a juegos numerados |
| Detectar error (`ERR-*`) | 3, 4, 7, 10 | `seed_logical_exercises.py`; `catalog.json`; contrato `FIND_ERROR` | Alta para compatibilidad del tipo | Sin confirmar: falta asignar los ejercicios a juegos numerados |

Estos candidatos no son una decisión de producto ni habilitan una ruta. No se encontró una fuente que indique qué prueba de los JSON corresponde a qué juego numerado.

### Registro de decisión por ejercicio

Los 200 ejercicios de las dos categorías recibidas tienen ID único. Cada fila es una decisión independiente: completar el número de juego, la fuente aprobadora y el estado únicamente al recibir evidencia autorizada. Hasta entonces, `SIN ASIGNAR`, `PENDIENTE` y `NO CONFIRMADO` son estados deliberados; no activan contenido. Para ordenación, los únicos candidatos técnicos son 1, 2 y 8; para detección, 3, 4, 7 y 10.

| ID del ejercicio | Juego aprobado (número) | Fuente de aprobación | Estado |
|---|---|---|---|
| `ORD-1-01` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-1-02` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-1-03` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-1-04` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-1-05` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-1-06` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-1-07` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-1-08` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-1-09` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-1-10` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-1-11` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-1-12` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-1-13` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-1-14` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-1-15` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-1-16` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-1-17` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-1-18` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-1-19` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-1-20` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-2-01` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-2-02` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-2-03` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-2-04` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-2-05` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-2-06` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-2-07` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-2-08` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-2-09` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-2-10` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-2-11` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-2-12` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-2-13` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-2-14` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-2-15` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-2-16` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-2-17` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-2-18` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-2-19` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-2-20` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-3-01` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-3-02` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-3-03` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-3-04` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-3-05` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-3-06` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-3-07` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-3-08` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-3-09` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-3-10` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-3-11` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-3-12` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-3-13` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-3-14` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-3-15` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-3-16` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-3-17` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-3-18` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-3-19` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-3-20` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-4-01` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-4-02` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-4-03` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-4-04` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-4-05` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-4-06` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-4-07` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-4-08` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-4-09` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-4-10` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-4-11` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-4-12` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-4-13` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-4-14` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-4-15` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-4-16` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-4-17` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-4-18` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-4-19` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-4-20` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-5-01` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-5-02` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-5-03` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-5-04` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-5-05` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-5-06` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-5-07` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-5-08` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-5-09` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-5-10` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-5-11` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-5-12` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-5-13` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-5-14` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-5-15` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-5-16` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-5-17` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-5-18` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-5-19` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ORD-5-20` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-1-01` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-1-02` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-1-03` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-1-04` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-1-05` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-1-06` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-1-07` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-1-08` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-1-09` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-1-10` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-1-11` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-1-12` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-1-13` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-1-14` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-1-15` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-1-16` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-1-17` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-1-18` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-1-19` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-1-20` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-2-01` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-2-02` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-2-03` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-2-04` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-2-05` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-2-06` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-2-07` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-2-08` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-2-09` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-2-10` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-2-11` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-2-12` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-2-13` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-2-14` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-2-15` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-2-16` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-2-17` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-2-18` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-2-19` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-2-20` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-3-01` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-3-02` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-3-03` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-3-04` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-3-05` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-3-06` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-3-07` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-3-08` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-3-09` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-3-10` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-3-11` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-3-12` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-3-13` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-3-14` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-3-15` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-3-16` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-3-17` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-3-18` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-3-19` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-3-20` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-4-01` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-4-02` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-4-03` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-4-04` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-4-05` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-4-06` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-4-07` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-4-08` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-4-09` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-4-10` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-4-11` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-4-12` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-4-13` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-4-14` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-4-15` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-4-16` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-4-17` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-4-18` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-4-19` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-4-20` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-5-01` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-5-02` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-5-03` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-5-04` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-5-05` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-5-06` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-5-07` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-5-08` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-5-09` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-5-10` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-5-11` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-5-12` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-5-13` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-5-14` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-5-15` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-5-16` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-5-17` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-5-18` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-5-19` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |
| `ERR-5-20` | SIN ASIGNAR | PENDIENTE | NO CONFIRMADO |

## Contratos confirmados y datos requeridos

- `ORDER_ALGORITHM`: el cliente envía `{"ordered_ids": [...]}`; el backend compara la lista con `expected_order`.
- `FIND_ERROR`: el cliente envía `{"selected_bug_id": "..."}`; el backend compara con `expected_bug_id`.
- `CONNECT_NETWORK`: el cliente envía `{"connections": [["id_a", "id_b"], ...]}`; el backend normaliza pares no dirigidos y compara con `expected_connections`.
- API de práctica provisional, fuera de `ExerciseType` y del ciclo diario:
  - `asociar_conceptos`: `{"asociaciones": [{"concepto": "<texto>", "explicacion": "<texto>"}]}`; exige coincidencia exacta de todas las parejas, sin crédito parcial.
  - `detectar_error`: `{"selected_line": "<texto exacto de la línea>"}`; el backend exige coincidencia única con la línea marcada en el JSON.
  - `ordenar_codigo`: `{"ordered_ids": ["<id de bloque>", ...]}`; compara el orden exacto con el dataset autorizado.
- `GET /provided-games/` lista los tres datasets y sus niveles. `GET /provided-games/<game_id>/<level>/` entrega una prueba aleatoria sin la solución. `POST` a esa ruta valida en servidor y devuelve la solución después del envío.
- Esta API no registra intentos, puntuación, XP, progreso por habilidad, racha ni recompensas. El estado provisional se muestra en el frontend y no cambia al jugar.
- Para cada variante de `CONNECT_NETWORK` (juegos 5, 6 y 9), el esquema actualmente validado requiere `instruction`, `prompt`, `content_version`, `validation_rules`, `error_explanation` y `provisional_notice` como strings no vacíos; `explanation` como string no vacío; e `input_data` como objeto.
- `nodes` debe ser una lista de al menos dos objetos `{ "id": string, "label": string }`, con IDs únicos y texto no vacío. `expected_connections` debe ser una lista no vacía de pares de dos strings; ambos IDs deben existir en `nodes`, ser distintos y no duplicar una conexión aunque se invierta el orden.
- La respuesta del cliente debe contener `connections`, una lista no vacía de pares de dos strings. El validador rechaza nodos iguales, pares duplicados y formatos inválidos; normaliza cada par como conexión no dirigida y exige igualdad exacta con `expected_connections`.
- La interfaz existente permite alternar conexiones seleccionando dos nodos; las respuestas esperadas y explicaciones no se envían en el contenido público.
- Para publicar cualquiera de ellos se requiere variante editorialmente aprobada, `variant_key` estable, versión y contenido estructural completo, incluida la respuesta esperada y las explicaciones obligatorias del esquema existente.
- El contrato descrito para `asociar_conceptos` solo cubre la práctica independiente solicitada y no se añade a `ExerciseType`. Para promoverlo al ciclo numerado se requiere aprobación de tipo/API, normalización, respuestas parciales, feedback, interfaz y reglas de intentos/progreso/puntuación.
- Para `CONNECT_NETWORK` faltan ejercicios aprobados completos: enunciado/instrucciones, nodos y etiquetas, conexiones correctas, explicación de solución y explicación de error.

Los registros históricos existentes no se borran ni se reescriben. El conteo del ciclo diario ahora excluye completaciones sin variante publicada, pero no se reconstruye el histórico agregado de `SkillProgress` a partir de variantes antiguas. Las rutas siguen siendo las existentes en `backend/apps/training/urls.py`; el cliente solo envía respuestas a la ruta de envío existente y el servidor determina la corrección. No se añadió una ruta alternativa de validación.

## Estado de los bloqueos

| Bloqueo | Estado | Motivo |
|---|---|---|
| `asociar_conceptos` | PARCIALMENTE RESUELTO | Ya se puede jugar mediante un endpoint y una UI independientes, con estado provisional; aprobación y contrato para cualquier integración al ciclo diario siguen pendientes. |
| Mapeo `ORD-*` / `ERR-*` | PARCIALMENTE RESUELTO | Los tres juegos se pueden jugar independientemente sin asignación numerada; el mapeo de los 200 IDs al ciclo diario continúa pendiente. |
| Contenido `CONNECT_NETWORK` | PARCIALMENTE RESUELTO | El contrato técnico existente queda documentado; faltan ejercicios completos y aprobación editorial para juegos 5, 6 y 9. |

La implementación de la práctica independiente está preparada para verificarse en el entorno local, pero no se ejecutaron pruebas end-to-end en esta fase. Antes de promover los datasets al ciclo oficial siguen pendientes la aprobación editorial y los mapeos por número; `asociar_conceptos` requiere además acuerdo de su contrato para dicho ciclo. No se ejecutaron Django, migraciones, pruebas automatizadas, instalación de paquetes ni build de React.
