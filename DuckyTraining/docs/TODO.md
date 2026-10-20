# TODO · Equipo 3 · DuckyTraining

## Estado implementado en el entorno provisional

- [x] Acceso diario: Free recibe tres juegos aleatorios del rango 1–6.
- [x] Acceso Plus/Pro y Alumno Plus temporal vigente a los diez juegos.
- [x] La vigencia temporal requiere una fecha de caducidad futura.
- [x] Los juegos seleccionados no requieren desbloqueo secuencial.
- [x] Máximo de cinco intentos por juego y día.
- [x] Fecha diaria basada en `Europe/Madrid` y `timezone.localdate()`.
- [x] Selección de Free guardada en el ciclo para que no cambie al refrescar.
- [x] Progreso por habilidad incrementado solo en el primer acierto diario de cada juego.
- [x] Racha actualizada una vez al completar todos los juegos seleccionados del ciclo.
- [x] `GET /api/training/progress/` e `GET /api/training/history/?limit=20`,
  ambos autenticados y filtrados por usuario.
- [x] Modelos sincronizados con el historial de migraciones. La migración 0008 añade
  la caducidad del acceso temporal y el indicador XP sin alterar las migraciones previas.
- [x] Migración 0009 normaliza el nombre y tipo del juego 10 como `Encuentra el fallo`.
- [x] XP definido como 5 por juego completado para Free, Plus, Pro y Alumno Plus
  temporal vigente; la concesión real permanece desactivada.
- [x] Interfaz conectada a overview/progreso/historial y envío de respuestas al servidor.
- [x] Login SimpleJWT con obtención/renovación de tokens y cabecera Bearer para Training.
- [x] Sin resultados aleatorios ni saldos ficticios de racha o Duki Coins.
- [x] Ejercicio 10 configurado como `Encuentra el fallo`.

## Pendiente de implementar el jueves 22

Mantener el entorno virtual provisional y no emitir recompensas reales hasta cerrar
los contratos con Equipo 5:

- [ ] Rewards: validación y evaluación inicial.
- [ ] Rewards persistente y servicio de procesamiento.
- [ ] Duki Bank y cartera de monedas.
- [ ] Acordar contratos, idempotencia, reintentos y protección frente a concesiones
  duplicadas.
- [ ] Activar concesión real de 5 XP solo después de aprobar los contratos de Rewards.
- [ ] Activar monedas únicamente cuando esté disponible el servicio acordado de
  Duki Bank.

## Pendiente de contenido educativo

- [ ] Completar y aprobar enunciados, respuestas correctas y explicaciones para los
  diez juegos.
- [ ] Publicar variantes en `backend/apps/training/content/catalog.json`.
- [ ] Validar en tests las respuestas correctas e incorrectas de cada variante.
- [ ] No quitar el estado de contenido pendiente ni simular validaciones mientras
  falten variantes educativas publicadas.

## Pendiente de integración

- [ ] Sustituir `UserTrainingProfile` provisional por el contrato de identidad/nivel
  de los equipos responsables.
- [ ] Acordar cómo se sincroniza la caducidad de Alumno Plus temporal.
- [ ] Validar con Equipo 5 los flujos de Rewards y Duki Bank antes de habilitarlos.

## Verificación local

Desde `backend`, ejecutar:

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test apps.training
```

Desde `frontend`, ejecutar:

```powershell
npm run build
```
