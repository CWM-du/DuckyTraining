# Fase 3 · Implementación base

## Alcance

Se implementó la base técnica de Equipo 3 · DuckyTraining conforme a `logica.md`, sin inventar contenido educativo ni contratos de otros equipos.

## Backend

- Django + Django REST Framework.
- Modelos para ciclo diario, progreso, intentos, variantes, habilidades, racha y logros.
- Niveles temporales y cupos 3/5/7/10.
- Estado secuencial de los ejercicios.
- Migración inicial.
- Endpoint de overview.
- Endpoint de envío preparado para aplicar validación server-side cuando existan las variantes y soluciones definitivas.

## Frontend

- React + Vite.
- Consulta del overview de Training.
- Presentación del nivel, cupo y estado de los ejercicios.

## Límites respetados

No se implementaron:

- preguntas o soluciones inventadas;
- importes de XP o DuckyCoins;
- contratos simulados de Equipos 0/5;
- formato inventado para el ejercicio 10;
- funcionalidades no autorizadas por `logica.md`.

## Verificación

La sintaxis de Python fue comprobada. La ejecución completa de Django y el build de React quedan pendientes de disponer de las dependencias del proyecto en un entorno con acceso a ellas.
