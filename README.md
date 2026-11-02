# Equipo 3 · DuckyTraining

Módulo de práctica individual de DuckyWorld/DuckyArenas. El alcance de este paquete es exclusivamente Equipo 3: catálogo y validación de ejercicios, ciclo diario, progreso, historial y adaptadores provisionales. La identidad/membresía oficial corresponde a Equipo 0/Core y las recompensas oficiales a Equipo 5; este repositorio no implementa internamente esos equipos.

## Estado y límites

- El catálogo define diez juegos y conserva los tipos de juego existentes: `ORDER_ALGORITHM`, `FIND_ERROR` y `CONNECT_NETWORK`.
- Las variantes actuales están marcadas **CONTENIDO EDUCATIVO PROVISIONAL — SUSTITUIR POR CONTENIDO APROBADO**. Son demostraciones técnicas, no contenido educativo definitivo, y el backend no las sirve ni valida como ejercicios jugables.
- Los tres JSON recibidos se pueden jugar desde una sección de práctica independiente, fuera del ciclo diario. Siguen etiquetados como provisionales y no se añaden al catálogo de los diez juegos.
- La práctica independiente usa una validación de servidor específica para esos datasets; `asociar_conceptos` no se añade a `ExerciseType` ni al contrato de los juegos numerados.
- Los contratos de `CONNECT_NETWORK` están implementados, pero no hay ejercicios educativos aprobados para sus juegos. Mientras no haya variantes `published`, estos juegos quedan como contenido pendiente y no pueden generar intentos correctos ni progreso nuevo.
- Las respuestas se validan en el backend. El cliente no envía una bandera de corrección.
- No se concede XP real ni Duki Coins. Las claves de evento son candidatas de integración, no confirmaciones de concesión.
- `UserTrainingProfile` y el adaptador de membresía son provisionales, no la fuente oficial de identidad o membresía.
- No se ha ejecutado Django, migraciones, tests ni el build de React durante esta revisión.

## Arquitectura actual

- `backend/apps/training/models.py`: ejercicios, ciclo diario, asignaciones de variante, intentos, progreso por habilidad y racha.
- `backend/apps/training/content/catalog.json`: contenido separado de las vistas y del motor de validación.
- `backend/apps/training/catalog.py`: carga, valida y asigna variantes estables por usuario/juego/mes.
- `backend/apps/training/provided_games.py`: carga los tres datasets de práctica provisional y valida sus respuestas sin modificar el ciclo diario.
- `backend/apps/training/validators.py`: validación de los tres formatos de juego.
- `backend/apps/training/views.py`: catálogo/ciclo, envío de respuesta, progreso e historial.
- `backend/apps/training/integrations/`: configuración JSON y adaptadores sustituibles de membresía y preparación de recompensas.
- `frontend/src/services/`: llamadas API y autenticación JWT.
- `frontend/src/components/training/`: interfaz de ciclo diario, área de práctica provisional y componentes de juego.

## Requisitos y configuración local

- Python compatible con las versiones de Django y DRF declaradas en `backend/requirements.txt`.
- Node.js/npm compatibles con el lockfile del frontend.
- `settings.py` lee `DJANGO_SECRET_KEY`, `DJANGO_DEBUG` y `DJANGO_ALLOWED_HOSTS` del entorno del proceso. `.env.example` es una plantilla informativa: Django no carga automáticamente archivos `.env` sin una dependencia adicional. En local, exporta esas variables desde tu terminal/IDE; nunca uses el valor de desarrollo en producción.
- Django ya está configurado con `TIME_ZONE = 'Europe/Madrid'` y `USE_TZ = True`. El ciclo diario usa `timezone.localdate()` y los timestamps se almacenan como datetimes conscientes de zona horaria. No reinterpretar datos históricos como si fueran horas locales sin una decisión de migración explícita.

## Configuración JSON de integraciones

Archivo: `backend/apps/training/integrations/config.json`.

Incluye `schema_version`, modo provisional, zona horaria, reglas de acceso, XP previsto, regla candidata de moneda e identificadores de proveedores pendientes. No debe contener credenciales ni secretos. El cargador valida la estructura y deshabilita la preparación de eventos si el JSON no es válido; un fallo de configuración de membresía nunca debe elevar privilegios. `grant_enabled` debe permanecer en `false` hasta aprobar los contratos oficiales.

La identidad/membresía oficial de Equipo 0/Core y el contrato de Rewards/Duki Bank de Equipo 5 siguen pendientes. No se han inventado endpoints ni llamadas internas de esos equipos.

## Sustituir contenido educativo

Editar `backend/apps/training/content/catalog.json` manteniendo `schema_version` y las diez entradas. Cada variante debe tener `variant_key` estable, estado, versión de contenido y un objeto `content` compatible con su `exercise_type`. Solo `status: "published"` habilita el juego; `provisional`, `pending_content` u otros estados no son ejecutables.

1. Mantener el esquema específico del juego: `steps` + `expected_order`, `code_items` + `expected_bug_id`, o `nodes` + `expected_connections`.
2. Incluir enunciado (`prompt`), instrucciones, `input_data`, reglas de validación, explicación del error, explicación de la solución y `content_version`.
3. Mientras el contenido sea de demostración, usar `status: "provisional"` y conservar el aviso literal de contenido provisional.
4. Tras aprobación editorial/pedagógica, sustituirlo por contenido aprobado y cambiar el estado a `published`. No marcar contenido como aprobado solo para habilitar el juego.
5. No cambiar el motor de validación para adaptar una pregunta concreta. Si cambia el contrato del formato, revisar código, frontend y pruebas de forma conjunta.
6. El backend elimina las respuestas esperadas y las explicaciones de solución del contenido público. Nunca añadir una respuesta correcta por defecto.

El validador verifica estructura e identificadores; no certifica calidad pedagógica ni exactitud curricular. El contenido provisional debe revisarse antes de cualquier despliegue educativo.

Los archivos de origen recibidos (`backend/apps/training/content/asociar_conceptos (1).json`, `backend/apps/training/content/detectar_error.json` y `backend/apps/training/content/ordenar_codigo (1).json`) no forman parte del ciclo diario: `catalog.py` carga exclusivamente `catalog.json`, mientras que `provided_games.py` los expone en una sección de práctica separada. Se muestran como **provisionales**. Si se propone incorporarlos al ciclo diario, aún hace falta aprobación editorial y una asignación aprobada a números de juego; `asociar_conceptos` necesitaría además aprobación de su contrato para esa integración.

### Práctica provisional de los tres datasets

Las rutas requieren autenticación JWT:

- `GET /api/training/provided-games/`: lista los tres juegos, instrucciones y niveles.
- `GET /api/training/provided-games/<game_id>/<level>/`: selecciona una prueba aleatoria del nivel y devuelve solo el contenido necesario para jugar, sin la respuesta correcta.
- `POST /api/training/provided-games/<game_id>/<level>/`: recibe `exercise_id` y `answer`; el backend obtiene la respuesta esperada del JSON fuente y devuelve corrección y solución únicamente después del envío.

Payloads de respuesta de práctica:

- `asociar_conceptos`: `{"asociaciones": [{"concepto": "<texto>", "explicacion": "<texto>"}]}`. Se exige el conjunto completo de parejas correctas; no hay puntuación parcial.
- `detectar_error`: `{"selected_line": "<texto exacto de la línea>"}`. Las líneas fuente son únicas en cada prueba.
- `ordenar_codigo`: `{"ordered_ids": ["<id de bloque>", ...]}`.

Este contrato sirve solo a la práctica provisional. No hay persistencia de intentos, puntuación, XP, progreso por habilidad, racha ni recompensas para esta sección; tampoco afecta las asignaciones mensuales. Las respuestas se validan en el servidor. No cambiar el estado editorial ni activar variantes `published` por el hecho de que estos datasets puedan jugarse aquí.

## Ciclo diario, acceso e intentos

- Free: tres juegos seleccionados aleatoriamente entre los juegos 1–6 y persistidos en el ciclo del usuario para el día local.
- Plus y Pro: acceso a los diez juegos.
- Alumno Plus temporal: acceso a los diez juegos solo mientras la caducidad exista y sea futura; sin vigencia verificable vuelve a Free.
- Máximo de cinco intentos por juego y ciclo diario. Los intentos se guardan con la corrección validada en servidor, variante y explicación.
- El primer acierto diario de un juego incrementa el progreso de habilidad una sola vez. Reintentos quedan en historial sin duplicar progreso.
- La racha se actualiza una vez cuando se completa la selección del ciclo. Si hay un día de interrupción, comienza una racha nueva al completar el siguiente ciclo.
- XP prevista: 5 por respuesta correcta para todos los niveles. Cada acierto puede preparar un evento candidato de XP; solo la primera finalización correcta de cada juego/día prepara la candidata a Duki Coin. No se concede ninguna recompensa real.

## Rutas disponibles

Todas las rutas de Training requieren autenticación JWT.

- `GET /api/training/`: catálogo y estado del ciclo diario.
- `POST /api/training/exercises/<exercise_number>/submit/`: valida y registra una respuesta.
- `GET /api/training/provided-games/` y `GET|POST /api/training/provided-games/<game_id>/<level>/`: práctica provisional independiente, sin registrar intentos o progreso diario.
- `GET /api/training/progress/`: progreso por habilidad y racha del usuario autenticado.
- `GET /api/training/history/?limit=20`: historial del usuario autenticado; `limit` admite enteros de 1 a 100.
- `POST /api/token/` y `POST /api/token/refresh/`: obtención y renovación de tokens SimpleJWT configuradas por el backend actual.

El servidor no acepta `user_id` del cliente para decidir qué datos puede consultar.

## Validación local posterior

No se ejecutaron estos comandos durante la revisión. Cuando recibas el ZIP, ejecútalos desde los directorios indicados.

Desde `DuckyTraining/backend`, con el entorno virtual activado:

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

`npm install` puede necesitar acceso al registro de paquetes. `npm run build` debe ejecutarse después de instalar las dependencias. Para desarrollo local, desde `backend` se puede ejecutar `python manage.py seed_logical_exercises` y después `python manage.py runserver`; desde `frontend`, `npm run dev`.

## Estado de verificación

Las comprobaciones estáticas que acompañan a esta entrega se describen en `docs/COMPARACION_REVISION.md`. La sintaxis estática y la estructura de JSON no sustituyen `manage.py check`, las migraciones, las pruebas Django ni el build real de React. Esos pasos quedan para la validación local indicada arriba.
