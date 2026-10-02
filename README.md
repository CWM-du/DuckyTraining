# Equipo 3 · DuckyTraining

Módulo individual de práctica de DuckyWorld/DuckyArenas.

## Estado

Base inicial creada a partir de `logica.md`. La definición funcional establece que la validación es de servidor, que los ejercicios diarios son secuenciales y que el estado educativo permanente se conserva aunque el ciclo diario se reinicie.

## Stack

- Frontend: React + Vite
- Backend: Python + Django + Django REST Framework
- Base de desarrollo: SQLite

## Alcance implementado en esta base

- Catálogo lógico de 10 ejercicios.
- Niveles temporales `FREE`, `ALUMNO_PLUS_TEMPORAL`, `PLUS`, `PRO`.
- Cupos diarios 3/5/7/10.
- Ciclo diario por usuario.
- Estados de ejercicio: disponible, bloqueado por secuencia, no accesible por nivel y completado hoy.
- Estructuras para variantes mensuales, intentos, progreso por habilidad, racha y logros.
- Frontend que muestra el estado del Training.

## Pendiente por especificación

- Contenido educativo definitivo, soluciones y explicaciones.
- Validadores de las variantes.
- Importes de XP y DuckyCoins.
- Contrato real con Equipos 0 y 5.
- Zona horaria oficial.
- Regla definitiva ante cambios de nivel durante un ciclo.
- Hitos concretos de racha y logros.
- Política de historial para reintentos tras completar un ejercicio el mismo día.
- Formato definitivo del ejercicio 10.

## Ejecución local

### Backend

```bash
cd backend
python -m venv .venv
# activar .venv según el sistema operativo
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

> La autenticación y el contrato final de identidad todavía dependen de la integración con el resto del proyecto.
