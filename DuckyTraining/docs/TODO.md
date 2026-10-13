# TODO · Equipo 3 · DuckyTraining

## Estado

- Fases 1–3: base técnica y auditoría previas.
- Fases 4–5: estructura técnica del catálogo JSON y del motor preparada; contenido educativo real pendiente. Ver `docs/FASE_4_5_ESTRUCTURA_TECNICA.md`.
- Fase 6: corrección estructural implementada; pendiente de validación local por el usuario y de contrato para cambios de membresía/recompensas.
- No se consideran terminados los puntos que dependen de contenido educativo validado o de contratos oficiales de otros equipos.

## Hecho

- [x] Estructura inicial React + Vite.
- [x] Estructura inicial Python + Django + Django REST Framework.
- [x] Modelo provisional de niveles de acceso: `FREE`, `ALUMNO_PLUS_TEMPORAL`, `PLUS` y `PRO`.
- [x] FREE: selección aleatoria y persistente de tres juegos entre 1–6 por ciclo diario.
- [x] PLUS/PRO: acceso al catálogo completo de diez juegos sin secuencia obligatoria.
- [x] `ALUMNO_PLUS_TEMPORAL`: se conserva el comportamiento heredado (cinco juegos secuenciales) hasta confirmación de Equipo 0.
- [x] Ciclo diario y selección en `Europe/Madrid`.
- [x] Modelo de progreso diario por ejercicio y control de Duki Coin por juego/ciclo.
- [x] Catálogo lógico de los 10 ejercicios definidos en `logica.md`.
- [x] Ejercicio 10 asignado a `FIND_ERROR` según decisión aprobada.
- [x] Modelos base para variantes mensuales, intentos, progreso por habilidad, racha y logros.
- [x] Migración inicial de Django incluida.
- [x] Comando de carga de ejercicios lógicos incluido.
- [x] Endpoint de consulta del estado diario.
- [x] Endpoint de envío conectado al catálogo JSON y a validadores server-side; requiere variantes publicadas para validar respuestas reales.
- [x] Plantilla de catálogo con 10 juegos y cinco espacios de variante por juego, sin contenido educativo inventado.
- [x] Validación estructural por formato y gestión explícita de variantes pendientes/configuración inválida.
- [x] README y documentación de la lógica aplicada.

## Tests a realizar

Esta sección concentra las comprobaciones que requieren un entorno con Python, Django y las dependencias del backend instaladas. No marcar un punto como realizado hasta ejecutar realmente el comando correspondiente.

### 1. Preparar entorno backend

Desde `DuckyTraining/backend`:

```bash
python -m venv .venv
```

Activar el entorno virtual:

**Windows PowerShell**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows CMD**

```cmd
.venv\Scripts\activate
```

**macOS/Linux**

```bash
source .venv/bin/activate
```

Instalar dependencias:

```bash
python -m pip install -r requirements.txt
```

### 2. Comprobación de Django

Verificar que Django está disponible:

```bash
python -m django --version
```

Comprobar la configuración del proyecto:

```bash
python manage.py check
```

**Resultado esperado:** `System check identified no issues`.

- [ ] `python manage.py check`

### 3. Comprobar migraciones

Revisar si existen migraciones pendientes:

```bash
python manage.py makemigrations --check --dry-run
```

**Resultado esperado:** Django no debe indicar migraciones pendientes.

Aplicar las migraciones en una base local de pruebas:

```bash
python manage.py migrate
```

- [ ] `python manage.py makemigrations --check --dry-run`
- [ ] `python manage.py migrate`

### 4. Cargar ejercicios lógicos

El proyecto contiene un comando para cargar el catálogo lógico de los ejercicios definidos en `logica.md`.

Ejecutar:

```bash
python manage.py seed_logical_exercises
```

Comprobar que el comando termina correctamente y que existen los ejercicios esperados.

**Importante:** este comando solo carga la definición lógica disponible. No crea preguntas educativas inventadas, soluciones definitivas ni variantes nuevas.

- [ ] `python manage.py seed_logical_exercises`

### 5. Tests automatizados de Django/DRF

Ejecutar la suite del proyecto:

```bash
python manage.py test
```

O específicamente los tests de Training:

```bash
python manage.py test training
```

Los tests actuales comprueban, entre otras cosas:

- que `FREE` reciba tres juegos aleatorios entre 1–6 y que la selección persista durante el ciclo;
- que los juegos seleccionados de `FREE` estén disponibles sin secuencia obligatoria;
- que `PLUS` y `PRO` tengan los diez juegos disponibles sin secuencia;
- que `ALUMNO_PLUS_TEMPORAL` conserve provisionalmente cinco juegos secuenciales;
- que los juegos no seleccionados de `FREE` se marquen como no accesibles.

- [ ] `python manage.py test`
- [ ] `python manage.py test training`

### 6. Comprobación manual de endpoints

Arrancar Django:

```bash
python manage.py runserver
```

Con un usuario de pruebas autenticado, comprobar el endpoint de overview:

```text
GET /api/training/overview/
```

Verificar que la respuesta refleja:

- nivel temporal;
- límite diario;
- ejercicios 1–10;
- estados de disponibilidad;
- selección aleatoria diaria y estados de disponibilidad por membresía.

El endpoint de envío de respuestas **no debe considerarse funcional** hasta que existan contenido educativo y validadores server-side aprobados.

- [ ] Arrancar `python manage.py runserver`.
- [ ] Verificar manualmente `GET /api/training/overview/`.
- [ ] Verificar autenticación y respuestas HTTP.

### 7. Tests de contenido educativo real pendientes

La estructura de catálogo está preparada, pero todas las variantes están pendientes de contenido. No ejecutar ni marcar como completados los tests pedagógicos hasta disponer de enunciados, soluciones, explicaciones y variantes validadas.

- [ ] Validar respuestas correctas de `Ordena el algoritmo`.
- [ ] Validar respuestas incorrectas de `Ordena el algoritmo` y explicación correspondiente.
- [ ] Validar `Encuentra el fallo`.
- [ ] Validar `Conecta la red`.
- [ ] Verificar que el servidor recupera la variante asignada y no confía en el cliente.
- [ ] Verificar que un fallo registra intento pero no concede XP ni desbloquea el siguiente ejercicio.
- [ ] Verificar que el primer acierto diario marca el ejercicio como completado.
- [ ] Verificar que cada partida completada emite el XP acordado mediante el contrato de Ecomotor; repetir un juego no concede otra Duki Coin ese día.
- [ ] Verificar que la selección Free permanece estable durante el día y se renueva al cambiar la fecha local.
- [x] Sustituir las reglas generales 3/5/7/10: Free 3 juegos aleatorios entre 1–6; Plus/Pro 10 juegos sin secuencia; `ALUMNO_PLUS_TEMPORAL` conserva provisionalmente su regla heredada de 5.
- [ ] Verificar en el entorno local el reinicio del ciclo en el cambio de día usando `Europe/Madrid`.
- [ ] Verificar variantes mensuales estables durante el mes.

### 8. Tests pendientes de integración con Equipo 0 y Equipo 5

No implementar contratos simulados como definitivos.

Cuando existan los contratos oficiales:

- [ ] Probar obtención del nivel efectivo desde Equipo 0/5 según el contrato aprobado.
- [ ] Verificar el ciclo diario y el límite de intentos alrededor del cambio de fecha en `Europe/Madrid`.
- [ ] Probar evento `TRAINING_EXERCISE_XP`.
- [ ] Probar evento `TRAINING_DAILY_COMPLETION`.
- [ ] Verificar protección contra duplicados.
- [ ] Verificar concurrencia y reenvíos.
- [ ] Verificar recepción de XP/DuckyCoins según el contrato real.
- [ ] Verificar logros globales si Equipo 5 los implementa.

## Tests frontend

Desde `DuckyTraining/frontend`:

Instalar dependencias:

```bash
npm install
```

Crear el build de producción:

```bash
npm run build
```

Arrancar desarrollo:

```bash
npm run dev
```

- [ ] `npm install`
- [ ] `npm run build`
- [ ] `npm run dev`
- [ ] Verificar visualmente estados disponible/bloqueado/no accesible/completado.
- [ ] Verificar que React no decide la corrección ni las recompensas.

## Pendientes funcionales antes de considerar DuckyTraining completo

- [x] Aplicar la zona horaria oficial acordada: `Europe/Madrid` (F6).
- [ ] Implementar la regla acordada para cambios de membresía durante un ciclo (F6/integración).
- [ ] Implementar XP acordada: 2 XP Free y 5 XP Plus/Pro por juego completado, mediante el contrato real.
- [ ] Implementar 1 Duki Coin por primera finalización diaria de cada juego distinto, mediante el contrato real de Duki Bank/Equipo 5.
- [ ] Validar enunciados, variantes, soluciones y explicaciones de los 10 ejercicios.
- [x] Definir el formato del ejercicio 10 como `FIND_ERROR`; queda pendiente crear y validar su contenido real.
- [ ] Definir hitos de logros; la regla base de racha diaria ya está aprobada e implementada.
- [x] Definir reintentos posteriores: se registran en historial, sin incrementar otra vez el progreso por habilidad en el mismo ciclo.
- [ ] Recibir contrato oficial de identidad/perfil de Equipo 0.
- [ ] Recibir contrato oficial de recompensas de Equipo 5.

## Implementación posterior

- [x] Implementar selección/asignación mensual server-side condicionada a que haya variantes publicadas.
- [x] Implementar validadores server-side estructurales para los tres formatos; validar resultados reales cuando se cargue contenido educativo.
- [x] Registrar intentos correctos/incorrectos en historial según la decisión aprobada.
- [x] Actualizar progreso por habilidad una sola vez por juego y ciclo diario; los reintentos posteriores solo se registran en el historial.
- [ ] Integrar XP mediante el contrato real de Equipo 5.
- [ ] Integrar finalización diaria y DuckyCoins mediante el contrato real de Equipo 5.
- [x] Implementar cálculo de racha al completar todo el cupo diario disponible, usando Europe/Madrid.
- [ ] Implementar logros según los hitos aprobados.
- [ ] Completar instrucciones y feedback de cada variante.

## Limitaciones conocidas de la Fase 3

- [x] La sintaxis Python fue comprobada con `compileall`.
- [ ] `manage.py check` requiere Django instalado.
- [ ] Migraciones requieren Django instalado.
- [ ] `manage.py test` requiere Django y dependencias instaladas.
- [ ] El build de React requiere instalar las dependencias npm.
- [ ] Las pruebas de integración con Equipo 0/5 no pueden completarse hasta disponer de sus contratos oficiales.

## Fase 6 · Implementación entregada para validación

- [x] Selección Free aleatoria entre juegos 1–6, guardada en el ciclo diario.
- [x] Acceso Plus/Pro al catálogo completo sin secuencia.
- [x] Estado `ALUMNO_PLUS_TEMPORAL` preservado como heredado, sin asignarle una regla nueva.
- [x] Zona horaria configurada como `Europe/Madrid`.
- [x] Migración añadida para la selección diaria y el indicador idempotente de Duki Coin.
- [ ] Ejecutar `makemigrations --check --dry-run`, `migrate`, `check` y tests en el entorno virtual del usuario.
- [ ] Validar los cambios de membresía intradía con el contrato oficial de Equipo 0/Ecomotor.
- [ ] Integrar el envío real de XP y Duki Coins solo tras recibir contratos oficiales.


## Fase 7 · Progreso e historial — revisión entregada

- [x] Mantener todos los intentos validados en el historial.
- [x] Incrementar progreso por habilidad solo en la primera finalización de cada juego por ciclo diario.
- [x] Actualizar racha una sola vez al completar el cupo diario disponible.
- [x] Añadir `GET /api/training/progress/` y `GET /api/training/history/`, filtrados por usuario autenticado.
- [x] Conectar React a las consultas de progreso e historial.
- [ ] Ejecutar comprobaciones Django y tests de F7 en el entorno virtual del usuario.
- [ ] Validar el comportamiento de extremo a extremo en frontend/backend.
- [ ] Definir logros solo cuando existan hitos aprobados.
- [ ] Integrar XP y Duki Coins únicamente con contratos oficiales.
