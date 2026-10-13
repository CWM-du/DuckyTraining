# Fases 4 y 5 · Estructura técnica del catálogo y motor

## Alcance de este cambio

Se prepara la infraestructura para recibir contenido educativo validado sin inventar enunciados, soluciones ni explicaciones. La fase 6 (selección diaria, membresías, cupos y zona horaria) no se modifica en este bloque.

## Catálogo JSON

Ruta: `backend/apps/training/content/catalog.json`.

- Define los 10 juegos y su formato.
- Reserva cinco claves de variante por juego (`exNN_v1` a `exNN_v5`).
- Todas las variantes empiezan con `status: "pending_content"` y `content: null`.
- No se consideran utilizables hasta tener `status: "published"` y un objeto `content` que supere la validación de estructura.
- El catálogo no contiene preguntas ficticias ni soluciones de ejemplo.

### Contrato de `content`

Todos los formatos requieren `instruction` y `explanation` como texto no vacío.

**ORDER_ALGORITHM**

- `steps`: lista no vacía de objetos `{ "id": string, "text": string }`, con identificadores únicos.
- `expected_order`: lista de identificadores que representa la solución correcta.

**FIND_ERROR**

- `code_items`: lista no vacía de objetos `{ "id": string, "text": string }`, con identificadores únicos.
- `expected_bug_id`: identificador existente en `code_items`.

**CONNECT_NETWORK**

- `nodes`: al menos dos objetos `{ "id": string, "label": string }`, con identificadores únicos.
- `expected_connections`: lista no vacía de pares `[id_a, id_b]`; los dos nodos deben existir, no pueden ser el mismo nodo y no se permiten pares duplicados.

La validación estructural no sustituye la revisión pedagógica humana del contenido.

## Resolución de variantes mensuales

`catalog.py` es responsable de leer el JSON, comprobar el contrato y escoger una variante publicada. La asignación se persiste por usuario, juego y primer día del mes para mantenerla estable durante ese mes. No se crean asignaciones si no hay variantes publicadas.

- Si no hay contenido publicado, el endpoint responde `503 variant_content_pending`.
- Si una asignación referencia una clave que no existe o contradice el juego/formato, responde `503 catalog_configuration_error`.
- El cliente no envía ni decide la solución; el servidor obtiene la variante desde el catálogo.

## Validación de respuestas

`validators.py` valida el tipo de entrada y evita aceptar respuestas vacías por defecto. Los tres validadores comparan la respuesta con la solución de la variante publicada. Las respuestas incorrectas incluyen la explicación configurada en el contenido.

El endpoint conserva el registro de intentos y el límite actual de cinco intentos por juego/ciclo. La garantía de concurrencia debe verificarse en el entorno Django/base de datos del proyecto; este cambio no afirma que los tests hayan sido ejecutados.

## Decisiones reflejadas

- El juego 10 queda asignado a `FIND_ERROR` según la decisión aprobada.
- `Difficulty` incorpora `EXPERT` además de los tres niveles existentes.
- No se implementan aquí la progresión automática de dificultad, la nueva selección aleatoria de Free, los cambios de membresía ni la zona horaria `Europe/Madrid`: estos últimos pertenecen a la revisión posterior de F6.

## Verificación

Se pueden realizar comprobaciones estáticas de sintaxis Python y validez JSON sin instalar dependencias. Para declarar completadas las pruebas de Django será necesario que el usuario las ejecute en su entorno virtual y comparta el resultado.
