import React, { useState } from 'react'
import ConnectNetworkGame from './ConnectNetworkGame'
import FindErrorGame from './FindErrorGame'
import OrderAlgorithmGame from './OrderAlgorithmGame'

const initialAnswer = (exercise) => {
  if (exercise.type === 'ORDER_ALGORITHM') {
    return { ordered_ids: exercise.content.steps.map((step) => step.id) }
  }
  if (exercise.type === 'FIND_ERROR') return { selected_bug_id: null }
  if (exercise.type === 'CONNECT_NETWORK') return { connections: [] }
  return {}
}

const ExerciseShell = ({ exercise, onClose, onSubmit }) => {
  const [phase, setPhase] = useState('INSTRUCTIONS')
  const [answer, setAnswer] = useState(() => initialAnswer(exercise))
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleSubmit = async () => {
    setPhase('VALIDATING')
    setError(null)
    try {
      const response = await onSubmit(exercise.number, answer)
      setResult(response)
      setPhase('FEEDBACK')
    } catch (submitError) {
      setError(submitError.message)
      setPhase('FEEDBACK')
    }
  }

  const game = exercise.type === 'ORDER_ALGORITHM'
    ? <OrderAlgorithmGame content={exercise.content} onAnswerChange={setAnswer} />
    : exercise.type === 'FIND_ERROR'
      ? <FindErrorGame content={exercise.content} onAnswerChange={setAnswer} />
      : exercise.type === 'CONNECT_NETWORK'
        ? <ConnectNetworkGame content={exercise.content} onAnswerChange={setAnswer} />
        : <p className="text-gray-600">Formato no disponible en este entorno provisional.</p>

  return (
    <div className="fixed inset-0 bg-gray-900/80 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <section className="bg-white w-full max-w-3xl rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        <header className="bg-gray-50 border-b border-gray-100 px-6 py-4 flex justify-between items-center">
          <div>
            <span className="text-xs font-bold text-gray-500 uppercase">Ejercicio {exercise.number}</span>
            <h2 className="text-xl font-bold text-gray-800">{exercise.name}</h2>
          </div>
          <button onClick={onClose} aria-label="Cerrar" className="rounded-full bg-gray-200 w-8 h-8">✕</button>
        </header>

        <div className="p-8 overflow-y-auto flex-grow">
          {phase === 'INSTRUCTIONS' && (
            <div className="text-center">
              <p className="text-gray-700 mb-6">{exercise.content.instruction}</p>
              <button
                onClick={() => setPhase('PLAYING')}
                className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-full"
              >
                Comenzar reto
              </button>
            </div>
          )}

          {phase === 'PLAYING' && (
            <>
              {game}
              <div className="mt-6 flex justify-end border-t pt-5">
                <button
                  onClick={handleSubmit}
                  disabled={exercise.type === 'FIND_ERROR' && !answer.selected_bug_id}
                  className="bg-gray-800 hover:bg-black disabled:opacity-40 text-white font-bold py-3 px-8 rounded-xl"
                >
                  Comprobar respuesta
                </button>
              </div>
            </>
          )}

          {phase === 'VALIDATING' && (
            <p className="text-center text-gray-600">Validando respuesta en el servidor…</p>
          )}

          {phase === 'FEEDBACK' && (
            <div role="status" className="text-center">
              {error ? (
                <>
                  <h3 className="text-2xl font-bold text-red-600 mb-3">No se pudo validar</h3>
                  <p className="text-gray-700 mb-6">{error}</p>
                  <button onClick={() => setPhase('PLAYING')} className="underline">Volver al juego</button>
                </>
              ) : result?.correct ? (
                <>
                  <h3 className="text-3xl font-black text-green-600 mb-4">¡Respuesta correcta!</h3>
                  <p className="text-gray-700 mb-2">
                    +{result.xp_per_completed_game} XP previstos; concesión pendiente de contrato.
                  </p>
                  <p className="text-sm text-amber-800 mb-6">
                    No se ha concedido XP real ni Duki Coins.
                  </p>
                  <button onClick={onClose} className="bg-green-600 text-white font-bold py-3 px-8 rounded-full">
                    Continuar
                  </button>
                </>
              ) : (
                <>
                  <h3 className="text-2xl font-bold text-red-600 mb-3">Respuesta incorrecta</h3>
                  <p className="text-gray-700 mb-6">{result?.explanation || 'Revisa la respuesta e inténtalo de nuevo.'}</p>
                  <button onClick={() => setPhase('PLAYING')} className="bg-gray-800 text-white font-bold py-3 px-8 rounded-full">
                    Intentarlo de nuevo
                  </button>
                </>
              )}
            </div>
          )}
        </div>
      </section>
    </div>
  )
}

export default ExerciseShell
