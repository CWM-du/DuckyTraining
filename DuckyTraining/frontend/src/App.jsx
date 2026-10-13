import { useEffect, useState } from 'react'
import { getTrainingOverview } from './services/trainingApi'

const stateLabels = {
  AVAILABLE: 'Disponible',
  BLOCKED_BY_SEQUENCE: 'Bloqueado por secuencia',
  NOT_ACCESSIBLE_BY_LEVEL: 'No accesible por nivel',
  COMPLETED_TODAY: 'Completado hoy',
}

export default function App() {
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    getTrainingOverview().then(setData).catch((e) => setError(e.message))
  }, [])

  if (error) return <main><h1>DuckyTraining</h1><p>No se pudo cargar Training: {error}</p></main>
  if (!data) return <main><h1>DuckyTraining</h1><p>Cargando…</p></main>

  return (
    <main>
      <header>
        <div><h1>DuckyTraining</h1><p>Práctica individual</p></div>
        <div className="summary"><strong>{data.access_level}</strong><span>{data.daily_limit} retos diarios</span></div>
      </header>
      <section>
        <h2>Retos de hoy</h2>
        <p>Fecha del ciclo: {data.cycle_date}</p>
        <div className="exercise-list">
          {data.exercises.map((exercise) => (
            <article key={exercise.number} className="exercise-card">
              <div><span className="number">{exercise.number}</span><h3>{exercise.name}</h3></div>
              <p>{exercise.type || 'Formato por confirmar'} · {exercise.difficulty}</p>
              <p>Habilidad: {exercise.skill}</p>
              <strong>{stateLabels[exercise.state] || exercise.state}</strong>
            </article>
          ))}
        </div>
      </section>
    </main>
  )
}
