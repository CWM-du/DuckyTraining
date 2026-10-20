# Fase 6 · Ciclo diario y acceso

## Reglas implementadas

- La fecha diaria usa `timezone.localdate()` con `Europe/Madrid`.
- Free recibe tres juegos aleatorios de los números 1–6. `DailyCycle.selected_exercises`
  conserva la selección para todo el ciclo local del día.
- Plus, Pro y Alumno Plus temporal vigente reciben los diez juegos activos. El nivel
  temporal requiere `access_expires_at` futuro; al caducar durante el día, el ciclo
  se ajusta a Free y obtiene una selección válida de tres juegos.
- Todos los juegos incluidos en la selección están disponibles sin desbloqueo
  secuencial.
- Se permiten hasta cinco intentos por juego y ciclo diario.
- Al cambiar la fecha local se crea un ciclo nuevo y se conserva el historial previo.

## Recompensas e integración

- El valor previsto es de 5 XP por juego completado para Free, Plus, Pro y Alumno
  Plus temporal vigente.
- La API deja claro que no concede XP real ni Duki Coins. Los indicadores
  `xp_reward_processed` y `ducky_coin_reward_processed` permanecen sin procesar.
- Rewards (validación/evaluación inicial, persistencia y servicio de procesamiento)
  y Duki Bank/cartera de monedas quedan **pendientes de implementar el jueves 22**.
- El nivel y la fecha de caducidad se mantienen en el perfil temporal hasta que se
  acuerde la fuente oficial de identidad/acceso.

## Configuración y validación

- El catálogo debe tener al menos tres juegos activos del rango Free (1–6) y los
  diez juegos activos para planes con acceso completo.
- Si el catálogo no cumple el mínimo, el endpoint devuelve un error explícito en
  lugar de crear una selección incompleta.
- Las variantes educativas pendientes no crean intentos ficticios y no pueden
  validar respuestas.
- Se añadieron pruebas de selección fija, acceso temporal vencido y las reglas de
  acceso; la ejecución está pendiente de autorización en el entorno local.
