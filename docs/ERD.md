# ERD · Equipo 3 · DuckyTraining

> Diseño técnico de la Fase 3. No añade reglas funcionales fuera de `logica.md`.

```mermaid
erDiagram
    USER ||--|| USER_TRAINING_PROFILE : has
    USER ||--o{ DAILY_CYCLE : owns
    USER ||--o{ MONTHLY_VARIANT_ASSIGNMENT : receives
    USER ||--o{ TRAINING_ATTEMPT : makes
    USER ||--o{ SKILL_PROGRESS : develops
    USER ||--|| TRAINING_STREAK : has
    USER ||--o{ TRAINING_ACHIEVEMENT : earns
    DAILY_CYCLE ||--o{ DAILY_EXERCISE_PROGRESS : contains
    DAILY_CYCLE }o--o{ EXERCISE : selects_for_free
    EXERCISE ||--o{ DAILY_EXERCISE_PROGRESS : tracked_in
    EXERCISE ||--o{ MONTHLY_VARIANT_ASSIGNMENT : assigned
    DAILY_CYCLE ||--o{ TRAINING_ATTEMPT : groups
    EXERCISE ||--o{ TRAINING_ATTEMPT : attempted

    USER_TRAINING_PROFILE {
        bigint id PK
        string access_level
        datetime access_expires_at
    }
    EXERCISE {
        bigint id PK
        smallint number UK
        string logical_name
        string exercise_type
        string difficulty
        string skill
        string introductory_relation
        boolean active
    }
    DAILY_CYCLE {
        bigint id PK
        date cycle_date
        string effective_access_level
        smallint daily_limit
        smallint completed_count
        boolean streak_processed
        relation selected_exercises
    }
    DAILY_EXERCISE_PROGRESS {
        bigint id PK
        boolean completed
        datetime completed_at
        boolean xp_reward_processed
        boolean ducky_coin_reward_processed
    }
    MONTHLY_VARIANT_ASSIGNMENT {
        bigint id PK
        date month
        string variant_key
    }
    TRAINING_ATTEMPT {
        bigint id PK
        datetime submitted_at
        json answer_payload
        boolean is_correct
        text error_explanation
    }
    SKILL_PROGRESS {
        bigint id PK
        string skill
        int successful_completions
    }
    TRAINING_STREAK {
        bigint id PK
        int current_streak
        date last_completion_date
    }
    TRAINING_ACHIEVEMENT {
        bigint id PK
        string achievement_key
        datetime granted_at
    }
```

## Borrado

- Datos dependientes del usuario: `CASCADE` al eliminar el usuario.
- Datos dependientes de `Exercise` y `DailyCycle`: `CASCADE`, porque en esta fase son registros internos de Training.
- Las reglas definitivas de retención, si otros equipos las requieren, quedan pendientes de contrato.

## Nota sobre usuarios

La guía PR07 propone una app `users` y un `CustomUser`. DuckyTraining no fija todavía ese contrato porque la especificación funcional asigna la identidad/autenticación definitiva a Equipo 0. Por tanto, se utiliza `AUTH_USER_MODEL` de Django como punto de integración y no se inventa un usuario definitivo.


## Reglas actualizadas 2026-10-20

- `UserTrainingProfile.access_level` distingue FREE/PLUS/PRO/ALUMNO_PLUS_TEMPORAL; no representa el nivel general.
- `DailyCycle.selected_exercises` conserva la selección diaria aleatoria de FREE (3 juegos entre los números 1–6).
- PLUS/PRO y Alumno Plus temporal vigente acceden al catálogo completo de diez juegos.
- El acceso temporal requiere `access_expires_at`; al caducar deja de habilitar el catálogo completo.
- Los indicadores `xp_reward_processed` y `ducky_coin_reward_processed` son independientes.
- El valor de XP es 5 por juego completado para los cuatro niveles; la concesión real permanece pendiente del contrato de Rewards/Equipo 5.
- El entorno no actualiza la wallet; Duki Bank y la cartera de monedas quedan pendientes de implementar el jueves 22.
