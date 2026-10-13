# Equipo 3 · DuckyTraining

Módulo individual de práctica de DuckyWorld/DuckyArenas.

## Estado

Base de Equipo 3 construida a partir de `logica.md`. F4 y F5 se consideran concluidas en su estado estructural; el contenido educativo real se incorporará a futuro. F6 incorpora selección diaria para Free y acceso completo para Plus/Pro. El estado heredado `ALUMNO_PLUS_TEMPORAL` conserva temporalmente sus reglas antiguas hasta confirmación de Equipo 0.

## Stack

- Frontend: React + Vite
- Backend: Python + Django + Django REST Framework
- Base de desarrollo: SQLite

## Alcance implementado en esta base

- Catálogo lógico de 10 ejercicios; el juego 10 utiliza `FIND_ERROR`.
- Plantilla JSON para cinco variantes por juego, sin enunciados ni soluciones inventadas.
- Validación estructural de variantes y respuestas en servidor.
- Asignación mensual estable solo para variantes publicadas.
- Niveles provisionales `FREE`, `ALUMNO_PLUS_TEMPORAL`, `PLUS`, `PRO`.
- FREE: tres juegos elegidos aleatoriamente entre los juegos 1–6, selección persistente por ciclo diario.
- PLUS/PRO: catálogo completo de diez juegos, sin secuencia obligatoria.
- `ALUMNO_PLUS_TEMPORAL`: reglas heredadas 5 juegos secuenciales, pendientes de confirmación de Equipo 0.
- Ciclo diario por usuario usando `Europe/Madrid`.
- Máximo de cinco intentos por juego y ciclo diario.
- Estructuras para variantes mensuales, intentos, progreso por habilidad, racha y logros.
- Frontend que muestra el estado del Training.

## Pendiente por especificación

- Contenido educativo definitivo, soluciones y explicaciones (las 50 variantes siguen pendientes).
- Revisión pedagógica de variantes y pruebas de respuestas reales.
- Importes de XP y DuckyCoins.
- Contrato real con Equipos 0 y 5.
- Integración definitiva de cambios de membresía durante el día, pendiente del contrato de Equipo 0/Ecomotor.
- Regla definitiva ante cambios de nivel durante un ciclo.
- Hitos concretos de racha y logros.
- Política de historial para reintentos tras completar un ejercicio el mismo día.

## Documentación de las fases 4 y 5

Consultar `docs/FASE_4_5_ESTRUCTURA_TECNICA.md` para el contrato del catálogo JSON, los campos requeridos por formato y el comportamiento cuando una variante aún no está publicada.

## Ejecución local

### Backend

```bash
cd backend
python -m venv .venv
# activar .venv según el sistema operativo
pip install -r requirements.txt
python manage.py makemigrations --check --dry-run
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

## Fase 6 · Ciclo diario y acceso

Consultar `docs/FASE_6_CICLO_DIARIO.md` para reglas implementadas, excepción heredada y comprobaciones pendientes. La integración de recompensas no se simula: XP depende de Ecomotor y Duki Coins de Duki Bank/Equipo 5.
