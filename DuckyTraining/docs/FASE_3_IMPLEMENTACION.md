# Fase 3 · Implementación técnica

## Implementado

- Backend Django + Django REST Framework y frontend React + Vite.
- Catálogo lógico de diez juegos y validación server-side contra variantes publicadas.
- Perfil provisional de acceso, ciclo diario, selección Free, intentos, progreso por
  habilidad e historial.
- Free recibe 3 juegos aleatorios del rango 1–6. Plus, Pro y Alumno Plus temporal
  vigente reciben los 10 juegos, sin desbloqueo secuencial.
- Se conserva el máximo de 5 intentos por juego y ciclo.
- Las migraciones 0001–0009 mantienen los modelos sincronizados, incluyendo
  `selected_exercises`, los indicadores separados de XP/monedas y la caducidad temporal.
- El frontend consume el overview, progreso e historial y envía las respuestas al
  backend; no genera resultados aleatorios.

## Pendiente

- Contenido educativo aprobado y variantes publicadas para los diez juegos.
- Contrato de identidad/acceso externo.
- Rewards: validación y evaluación inicial, persistencia y servicio de procesamiento.
- Duki Bank y cartera de monedas.
- Habilitar recompensas reales solo después de acordar las integraciones con Equipo 5.

Los trabajos de Rewards y Duki Bank están **pendientes de implementar el jueves 22**.
El entorno continúa siendo provisional; no se conceden XP ni monedas reales.

## Verificación

Se añadieron tests para las reglas de acceso, XP en estado pendiente, intentos,
progreso, racha y aislamiento por usuario. La ejecución de tests y build debe
confirmarse en el entorno del proyecto; esta documentación no marca resultados no
ejecutados.
