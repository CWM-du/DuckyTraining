# TODO · Equipo 3 · DuckyTraining

## Implementado en código (pendiente de ejecución local)

- [x] Ciclo diario con selección Free aleatoria entre juegos 1–6 y persistencia en `DailyCycle.selected_exercises`.
- [x] Plus/Pro y Alumno Plus temporal vigente con selección de diez juegos; el acceso temporal exige caducidad futura.
- [x] Límite de cinco intentos por juego/ciclo y registro de intentos correctos e incorrectos.
- [x] Progreso de habilidad solo en el primer acierto diario por juego.
- [x] Racha procesada una vez al completar todos los juegos seleccionados.
- [x] Rutas autenticadas de progreso e historial, filtradas por `request.user` y con límite de historial validado.
- [x] Zona horaria Django `Europe/Madrid` con `USE_TZ = True`.
- [x] Adaptadores sustituibles de membresía y preparación de eventos de recompensa; no conceden recompensas reales.
- [x] Configuración JSON provisional validada y sin secretos.
- [x] Diez variantes de demostración marcadas como contenido educativo provisional y validadas por tipo de juego; solo las variantes `published` son ejecutables.
- [x] Frontend consume la API backend y muestra el estado pendiente cuando no hay una variante publicada.
- [x] Se habilitó un área autenticada de práctica independiente para los tres JSON proporcionados; conserva la etiqueta provisional, valida respuestas en servidor y no modifica ciclo diario ni progreso.

## Revisado estáticamente

- [x] Se compararon el ZIP remoto (identificado por el repositorio `.git` y la rama `feature_hugo`) y el ZIP de revisión sin `.git`.
- [x] Se inspeccionaron modelos y migraciones 0001–0009; el campo `selected_exercises`, los flags de XP/moneda y la caducidad temporal aparecen alineados en la cadena declarada, sin añadir una migración correctiva innecesaria.
- [x] Se validó estáticamente que las rutas de progreso e historial existen en `apps/training/urls.py`.
- [x] Se comprobaron sintaxis Python, parseo JSON, unicidad de identificadores del catálogo e integridad del ZIP final.
- [x] Se documentó el inventario de los diez juegos y sus variantes (`variant_key`, versión, estado y origen conocido), separando demos del catálogo de runtime y datasets recibidos sin aprobación.
- [x] Se registraron individualmente los 200 IDs `ORD-*` y `ERR-*` con mapeo, fuente de aprobación y estado aún sin confirmar; los números candidatos no están activados como asignaciones.
- [x] Se documentó el contrato actual de `CONNECT_NETWORK` y se implementó un contrato de práctica provisional aislado para `asociar_conceptos`, sin añadirlo a `ExerciseType`.
- [x] Se inspeccionó estáticamente el flujo para confirmar que solo variantes publicadas se seleccionan, se sirven y se validan; las no publicadas no crean nuevos intentos ni completaciones.
- [x] Se confirmó que los registros históricos no se borran ni reescriben; los agregados históricos de `SkillProgress` no se recalculan en esta fase.
- [x] En esta revisión se analizaron los cuatro JSON con parser estándar, se comprobó el AST de `catalog.py`, `views.py` y `tests.py`, y se verificaron la unicidad/estructura de los IDs, las 200 filas del registro de asignación y `git diff --check` en `docs/TODO.md`. También se revisaron manualmente los espacios finales del documento de comparación, que aún no está rastreado por Git.
- [ ] Verificar manualmente las nuevas rutas y la interfaz de práctica cuando se autorice ejecutar el entorno; no se ejecutaron servicios ni pruebas en esta fase.
- [ ] No se ha ejecutado Django ni se ha verificado el estado real de migraciones contra una base de datos.

## Pendiente de validación local

- [ ] `python manage.py check`.
- [ ] `python manage.py makemigrations --check --dry-run`.
- [ ] `python manage.py migrate`.
- [ ] `python manage.py test apps.training`.
- [ ] `npm install` y `npm run build`.
- [ ] Verificación manual del ciclo Free, caducidad temporal, concurrencia, intentos, progreso, historial y racha.

## Pendiente de contenido educativo aprobado

- [ ] Sustituir cada variante de demostración por contenido aprobado por la persona/equipo responsable.
- [ ] Revisar pedagógicamente enunciados, datos, soluciones y explicaciones de los diez juegos.
- [ ] Añadir y ejecutar pruebas de aceptación para respuestas correctas e incorrectas de cada variante aprobada.
- [ ] No quitar la etiqueta provisional hasta que exista aprobación real.
- [ ] Resolver la asignación de los 100 ejercicios `ORD-*` y `ERR-*` a números concretos; los tipos compatibles solo permiten candidatos (orden: 1, 2, 8; error: 3, 4, 7, 10), no un mapeo aprobado.
- [ ] Si se quiere incorporar la práctica al ciclo numerado, aprobar el mapeo de los 100 IDs `ORD-*` y `ERR-*` y formalizar el contrato de práctica de `asociar_conceptos` para ese ciclo.
- [ ] Proporcionar contenido educativo aprobado completo para `CONNECT_NETWORK` (juegos 5, 6 y 9).
- [ ] Aprobar editorialmente los datasets provisionales antes de publicar contenido educativo oficial.
- [ ] Ejecutar pruebas end-to-end en el entorno local después de la validación técnica; no se ejecutaron en esta fase.
- [ ] Antes de pasar una variante a `published`, registrar la fuente de aprobación editorial; el estado del catálogo por sí solo no acredita aprobación.

## Pendiente de integración oficial

Mantener estos tres puntos con el comentario literal **“Pendiente de implementar el jueves 22”**:

- [ ] **Pendiente de implementar el jueves 22** — Rewards: validación y evaluación inicial.
- [ ] **Pendiente de implementar el jueves 22** — Rewards persistente y servicio de procesamiento.
- [ ] **Pendiente de implementar el jueves 22** — Duki Bank y cartera de monedas.

- [ ] Contrato oficial de identidad/membresía de Equipo 0/Core.
- [ ] Contrato de Rewards de Equipo 5: idempotencia, reintentos, confirmación de concesión y errores.
- [ ] Integración oficial de Duki Bank. No crear una cartera local ni mostrar saldo oficial sin fuente acordada.
- [ ] No conceder XP mediante Ecomotor ni marcar eventos como concedidos sin contrato y confirmación oficiales.

## Pendiente de decisión o contrato externo

- [ ] Acordar si las claves candidatas de recompensa se persistirán en un outbox local y qué servicio será responsable de procesarlas.
- [ ] Confirmar las reglas de expiración y sincronización del Alumno Plus temporal con Equipo 0/Core.
- [ ] Confirmar el contrato final del historial/progreso si otros equipos necesitan consumirlo.
