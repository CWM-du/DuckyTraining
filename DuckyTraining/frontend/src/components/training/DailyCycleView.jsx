import React, { useState } from 'react'
import ExerciseShell from './ExerciseShell'

const DailyCycleView = ({ data, progress, history, onRefresh, onExerciseSubmit }) => {
  const { access_level, daily_limit, cycle_date, completed_count, exercises } = data
  const [activeExercise, setActiveExercise] = useState(null)

  const renderExerciseState = (exercise) => {
    switch (exercise.state) {
      case 'COMPLETED_TODAY':
        return <span className="font-bold text-green-600">Completado</span>
      case 'AVAILABLE':
        return (
          <button
            onClick={() => setActiveExercise(exercise)}
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-full"
          >
            ¡Jugar!
          </button>
        )
      case 'CONTENT_PENDING':
        return <span className="text-sm text-amber-700">Contenido educativo pendiente</span>
      case 'NOT_ACCESSIBLE_BY_LEVEL':
        return <span className="text-sm text-gray-500">No incluido en la selección de hoy</span>
      default:
        return null
    }
  }

  return (
    <main className="max-w-5xl mx-auto p-6 bg-gray-50 min-h-screen">
      <aside className="mb-6 rounded-xl border border-amber-300 bg-amber-50 p-4 text-sm text-amber-950">
        <strong>Entorno virtual provisional.</strong> Rewards (validación y evaluación inicial,
        persistencia y servicio de procesamiento) y Duki Bank/cartera de monedas: «Pendiente de
        implementar el jueves 22». No se conceden recompensas ni monedas reales hasta acordar
        los contratos de integración con Equipo 5.
      </aside>

      <header className="bg-white rounded-2xl shadow-sm p-6 mb-8 border border-gray-100">
        <div className="flex flex-wrap justify-between gap-6 items-center">
          <div>
            <h1 className="text-3xl font-extrabold text-gray-800">DuckyTraining</h1>
            <p className="text-gray-500 mt-1">Práctica individual · Fecha: {cycle_date}</p>
          </div>
          <div className="flex flex-wrap gap-4 text-center">
            <div className="bg-orange-100 px-4 py-2 rounded-lg">
              <p className="text-xs text-orange-700 font-bold uppercase">Racha</p>
              <p className="text-2xl font-black text-orange-600">
                {progress?.streak.current ?? '—'}
              </p>
            </div>
            <div className="bg-purple-100 px-4 py-2 rounded-lg">
              <p className="text-xs text-purple-700 font-bold uppercase">Plan</p>
              <p className="text-2xl font-black text-purple-700">{access_level}</p>
              <p className="text-xs text-purple-500">{daily_limit} juegos diarios</p>
            </div>
            <div className="bg-blue-100 px-4 py-2 rounded-lg">
              <p className="text-xs text-blue-700 font-bold uppercase">Progreso diario</p>
              <p className="text-2xl font-black text-blue-700">{completed_count}/{daily_limit}</p>
              <p className="text-xs text-blue-500">5 XP por juego completado · concesión pendiente</p>
            </div>
          </div>
        </div>
      </header>

      <section aria-label="Juegos del ciclo diario" className="space-y-4">
        {exercises.map((exercise) => {
          const isCompleted = exercise.state === 'COMPLETED_TODAY'
          return (
            <article
              key={exercise.number}
              className={`flex items-center justify-between gap-4 p-6 rounded-2xl border-2 ${
                isCompleted ? 'bg-green-50 border-green-200' : 'bg-white border-gray-100'
              }`}
            >
              <div className="flex items-center gap-4">
                <div className={`w-12 h-12 flex items-center justify-center rounded-full font-black text-lg ${
                  isCompleted ? 'bg-green-200 text-green-700' : 'bg-blue-100 text-blue-600'
                }`}>
                  {exercise.number}
                </div>
                <div>
                  <h2 className="text-xl font-bold text-gray-800">{exercise.name}</h2>
                  <p className="text-sm text-blue-600">
                    {exercise.type?.replaceAll('_', ' ') || 'Formato por confirmar'} · {exercise.skill}
                  </p>
                  <p className="text-xs text-gray-500">{exercise.difficulty}</p>
                </div>
              </div>
              {renderExerciseState(exercise)}
            </article>
          )
        })}
      </section>

      <section className="grid gap-6 md:grid-cols-2 mt-10">
        <div className="bg-white rounded-2xl border border-gray-100 p-6">
          <h2 className="text-xl font-bold mb-3">Progreso por habilidad</h2>
          {progress?.skills?.length ? (
            <ul className="space-y-2">
              {progress.skills.map((skill) => (
                <li key={skill.skill} className="flex justify-between">
                  <span>{skill.skill}</span>
                  <span>{skill.successful_completions} juegos completados</span>
                </li>
              ))}
            </ul>
          ) : <p className="text-gray-500">Aún no hay juegos completados.</p>}
        </div>
        <div className="bg-white rounded-2xl border border-gray-100 p-6">
          <div className="flex justify-between items-center mb-3">
            <h2 className="text-xl font-bold">Historial</h2>
            <button onClick={onRefresh} className="text-sm text-blue-600 underline">Actualizar</button>
          </div>
          {history.length ? (
            <ul className="space-y-2">
              {history.map((attempt, index) => (
                <li key={`${attempt.exercise_number}-${attempt.submitted_at}-${index}`} className="text-sm">
                  {attempt.cycle_date} · Juego {attempt.exercise_number} · Intento {attempt.attempt_number} · {attempt.is_correct ? 'Correcto' : 'Incorrecto'}
                </li>
              ))}
            </ul>
          ) : <p className="text-gray-500">Todavía no hay intentos registrados.</p>}
        </div>
      </section>

      {activeExercise && (
        <ExerciseShell
          exercise={activeExercise}
          onClose={() => setActiveExercise(null)}
          onSubmit={onExerciseSubmit}
        />
      )}
    </main>
  )
}

export default DailyCycleView
