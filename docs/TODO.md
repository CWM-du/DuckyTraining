# TODO · Equipo 3 · DuckyTraining

## Estado

- Fase 3: base técnica creada.
- La lógica funcional se rige por `docs/LOGICA_APLICADA.md` y `logica.md`.
- No se consideran terminados los puntos que dependen de contenido educativo validado o de contratos oficiales de otros equipos.

## Hecho

- [x] Estructura inicial React + Vite.
- [x] Estructura inicial Python + Django + Django REST Framework.
- [x] Modelo de niveles temporales: `FREE`, `ALUMNO_PLUS_TEMPORAL`, `PLUS` y `PRO`.
- [x] Límites diarios 3/5/7/10.
- [x] Modelo de ciclo diario y fijación temporal del nivel al crear el ciclo.
- [x] Modelo de progreso diario por ejercicio.
- [x] Estados de ejercicios: disponible, bloqueado por secuencia, no accesible por nivel y completado hoy.
- [x] Catálogo lógico de los 10 ejercicios definidos en `logica.md`.
- [x] Ejercicio 10 sin formato inventado; queda pendiente de definición.
- [x] Modelos base para variantes mensuales, intentos, progreso por habilidad, racha y logros.
- [x] Migración inicial de Django incluida.
- [x] Comando de carga de ejercicios lógicos incluido.
- [x] Endpoint de consulta del estado diario.
- [x] Endpoint estructural de envío de respuestas con validación educativa pendiente.
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

- que un usuario `FREE` tenga un límite diario de 3;
- que el primer ejercicio esté disponible;
- que el siguiente quede bloqueado hasta completar el anterior;
- que los ejercicios fuera del nivel estén marcados como no accesibles;
- que completar un ejercicio desbloquee el siguiente.

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
- secuencia diaria.

El endpoint de envío de respuestas **no debe considerarse funcional** hasta que existan contenido educativo y validadores server-side aprobados.

- [ ] Arrancar `python manage.py runserver`.
- [ ] Verificar manualmente `GET /api/training/overview/`.
- [ ] Verificar autenticación y respuestas HTTP.

### 7. Tests pendientes cuando exista contenido educativo

No ejecutar ni marcar como completados hasta disponer de enunciados, soluciones, explicaciones y variantes validadas.

- [ ] Validar respuestas correctas de `Ordena el algoritmo`.
- [ ] Validar respuestas incorrectas de `Ordena el algoritmo` y explicación correspondiente.
- [ ] Validar `Encuentra el fallo`.
- [ ] Validar `Conecta la red`.
- [ ] Verificar que el servidor recupera la variante asignada y no confía en el cliente.
- [ ] Verificar que un fallo registra intento pero no concede XP ni desbloquea el siguiente ejercicio.
- [ ] Verificar que el primer acierto diario marca el ejercicio como completado.
- [ ] Verificar que un segundo acierto el mismo día no genera XP adicional.
- [ ] Verificar el desbloqueo secuencial.
- [ ] Verificar los límites diarios 3/5/7/10.
- [ ] Verificar reinicio del ciclo en el cambio de día según la zona horaria oficial.
- [ ] Verificar variantes mensuales estables durante el mes.

### 8. Tests pendientes de integración con Equipo 0 y Equipo 5

No implementar contratos simulados como definitivos.

Cuando existan los contratos oficiales:

- [ ] Probar obtención del nivel efectivo desde Equipo 0/5 según el contrato aprobado.
- [ ] Probar la zona horaria oficial del ciclo diario.
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

- [ ] Confirmar zona horaria oficial con Equipo 0.
- [ ] Confirmar definitivamente la regla de cambio de nivel durante un ciclo.
- [ ] Definir importes de XP con Equipo 5.
- [ ] Definir DuckyCoins con Equipo 5.
- [ ] Validar enunciados, variantes, soluciones y explicaciones de los 10 ejercicios.
- [ ] Definir el formato del ejercicio 10 sin salir de los tres formatos autorizados, salvo nueva autorización.
- [ ] Definir hitos concretos de racha y logros.
- [ ] Definir cómo se registran reintentos posteriores a un ejercicio ya completado ese día.
- [ ] Recibir contrato oficial de identidad/perfil de Equipo 0.
- [ ] Recibir contrato oficial de recompensas de Equipo 5.

## Implementación posterior

- [ ] Implementar selección mensual de variantes en servidor una vez exista contenido educativo.
- [ ] Implementar validadores server-side por formato y variante.
- [ ] Registrar intentos correctos/incorrectos según la decisión definitiva de historial.
- [ ] Actualizar progreso por habilidad tras un acierto válido.
- [ ] Integrar XP mediante el contrato real de Equipo 5.
- [ ] Integrar finalización diaria y DuckyCoins mediante el contrato real de Equipo 5.
- [ ] Implementar cálculo de racha según las reglas aprobadas.
- [ ] Implementar logros según los hitos aprobados.
- [ ] Completar instrucciones y feedback de cada variante.

## Limitaciones conocidas de la Fase 3

- [x] La sintaxis Python fue comprobada con `compileall`.
- [ ] `manage.py check` requiere Django instalado.
- [ ] Migraciones requieren Django instalado.
- [ ] `manage.py test` requiere Django y dependencias instaladas.
- [ ] El build de React requiere instalar las dependencias npm.
- [ ] Las pruebas de integración con Equipo 0/5 no pueden completarse hasta disponer de sus contratos oficiales.
