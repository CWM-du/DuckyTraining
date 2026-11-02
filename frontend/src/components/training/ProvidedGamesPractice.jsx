import { useEffect, useState } from 'react'
import {
  getProvidedGameChallenge,
  getProvidedGames,
  submitProvidedGameAnswer,
} from '../../services/trainingApi'

const ProvidedGamesPractice = () => {
  const [games, setGames] = useState([])
  const [selectedGame, setSelectedGame] = useState(null)
  const [selectedLevel, setSelectedLevel] = useState(null)
  const [challenge, setChallenge] = useState(null)
  const [associationPairs, setAssociationPairs] = useState([])
  const [selectedConcept, setSelectedConcept] = useState(null)
  const [selectedExplanation, setSelectedExplanation] = useState(null)
  const [orderedIds, setOrderedIds] = useState([])
  const [selectedLine, setSelectedLine] = useState(null)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)

  useEffect(() => {
    let active = true
    getProvidedGames()
      .then(({ games: availableGames }) => {
        if (active) setGames(availableGames)
      })
      .catch((requestError) => {
        if (active) setError(requestError.message)
      })
      .finally(() => {
        if (active) setIsLoading(false)
      })
    return () => {
      active = false
    }
  }, [])

  const loadChallenge = async () => {
    if (!selectedGame || selectedLevel === null) return
    setIsLoading(true)
    setError(null)
    setChallenge(null)
    setResult(null)
    try {
      const nextChallenge = await getProvidedGameChallenge(selectedGame.id, selectedLevel)
      setChallenge(nextChallenge)
      setAssociationPairs([])
      setSelectedConcept(null)
      setSelectedExplanation(null)
      setOrderedIds(nextChallenge.content.bloques?.map((block) => block.id) ?? [])
      setSelectedLine(null)
    } catch (requestError) {
      setError(requestError.message)
    } finally {
      setIsLoading(false)
    }
  }

  const selectConcept = (conceptId) => {
    setAssociationPairs((pairs) => pairs.filter((pair) => pair.concepto !== conceptId))
    if (selectedConcept === conceptId) {
      setSelectedConcept(null)
      return
    }
    if (selectedExplanation) {
      setAssociationPairs((pairs) => [
        ...pairs.filter((pair) => pair.explicacion !== selectedExplanation),
        { concepto: conceptId, explicacion: selectedExplanation },
      ])
      setSelectedConcept(null)
      setSelectedExplanation(null)
      return
    }
    setSelectedConcept(conceptId)
  }

  const selectExplanation = (explanationId) => {
    setAssociationPairs((pairs) => pairs.filter((pair) => pair.explicacion !== explanationId))
    if (selectedExplanation === explanationId) {
      setSelectedExplanation(null)
      return
    }
    if (selectedConcept) {
      setAssociationPairs((pairs) => [
        ...pairs.filter((pair) => pair.concepto !== selectedConcept),
        { concepto: selectedConcept, explicacion: explanationId },
      ])
      setSelectedConcept(null)
      setSelectedExplanation(null)
      return
    }
    setSelectedExplanation(explanationId)
  }

  const moveBlock = (index, direction) => {
    const targetIndex = index + direction
    if (targetIndex < 0 || targetIndex >= orderedIds.length) return
    setOrderedIds((ids) => {
      const updated = [...ids]
      const current = updated[index]
      updated[index] = updated[targetIndex]
      updated[targetIndex] = current
      return updated
    })
  }

  const submitAnswer = async () => {
    if (!challenge || !selectedGame || selectedLevel === null) return
    let answer
    if (selectedGame.id === 'asociar_conceptos') {
      answer = { asociaciones: associationPairs }
    } else if (selectedGame.id === 'detectar_error') {
      answer = { selected_line: selectedLine }
    } else {
      answer = { ordered_ids: orderedIds }
    }
    setIsSubmitting(true)
    setError(null)
    try {
      setResult(await submitProvidedGameAnswer(
        selectedGame.id,
        selectedLevel,
        challenge.exercise_id,
        answer,
      ))
    } catch (requestError) {
      setError(requestError.message)
    } finally {
      setIsSubmitting(false)
    }
  }

  const answerIsReady = () => {
    if (!challenge || !selectedGame) return false
    if (selectedGame.id === 'asociar_conceptos') {
      return associationPairs.length === challenge.content.conceptos.length
    }
    if (selectedGame.id === 'detectar_error') return selectedLine !== null
    return orderedIds.length > 0
  }

  return (
    <section aria-label="Juegos de práctica adicionales" className="mt-10">
      <header className="mb-4">
        <h2 className="text-2xl font-extrabold text-gray-800">Juegos de práctica</h2>
        <p className="mt-1 text-sm text-gray-600">
          Estos tres juegos usan los datasets proporcionados y están marcados como provisionales.
          Sus resultados no cambian el ciclo diario, el progreso, la racha ni las recompensas.
        </p>
      </header>

      {isLoading && games.length === 0 && (
        <p role="status" className="rounded-lg bg-white p-4 text-gray-600">
          Cargando juegos de práctica…
        </p>
      )}
      {error && <p role="alert" className="mb-4 rounded-lg bg-red-100 p-3 text-red-800">{error}</p>}

      <div className="grid gap-4 md:grid-cols-3">
        {games.map((game) => (
          <button
            key={game.id}
            type="button"
            onClick={() => {
              setSelectedGame(game)
              setSelectedLevel(game.levels[0] ?? null)
              setChallenge(null)
              setResult(null)
              setError(null)
            }}
            aria-pressed={selectedGame?.id === game.id}
            className={`rounded-xl border-2 bg-white p-5 text-left shadow-sm ${
              selectedGame?.id === game.id ? 'border-blue-500' : 'border-gray-200'
            }`}
          >
            <span className="text-xs font-bold uppercase text-amber-800">Provisional</span>
            <h3 className="mt-2 text-lg font-bold text-gray-800">{game.name}</h3>
            <p className="mt-2 text-sm text-gray-600">{game.instruction}</p>
          </button>
        ))}
      </div>

      {selectedGame && (
        <div className="mt-5 rounded-xl border border-gray-200 bg-white p-5">
          <div className="flex flex-wrap items-center gap-2">
            <span className="font-semibold text-gray-800">Nivel:</span>
            {selectedGame.levels.map((level) => (
              <button
                key={level}
                type="button"
                onClick={() => {
                  setSelectedLevel(level)
                  setChallenge(null)
                  setResult(null)
                }}
                aria-pressed={selectedLevel === level}
                className={`rounded-full px-4 py-2 text-sm font-semibold ${
                  selectedLevel === level ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700'
                }`}
              >
                {level}
              </button>
            ))}
            {!challenge && (
              <button
                type="button"
                onClick={loadChallenge}
                disabled={isLoading || selectedLevel === null}
                className="ml-auto rounded-full bg-gray-800 px-5 py-2 font-bold text-white disabled:opacity-50"
              >
                {isLoading ? 'Cargando…' : 'Comenzar'}
              </button>
            )}
          </div>

          {challenge && (
            <div className="mt-6 border-t border-gray-100 pt-5">
              <p className="text-sm text-gray-500">
                Prueba {challenge.exercise_id} · Nivel {challenge.level}
              </p>

              {selectedGame.id === 'asociar_conceptos' && (
                <>
                  <p className="mt-4 text-sm text-gray-600">
                    Selecciona un concepto y después su explicación para formar cada pareja.
                  </p>
                  <div className="mt-3 grid gap-6 md:grid-cols-2">
                    <div className="space-y-2">
                      <h4 className="font-bold text-gray-700">Conceptos</h4>
                      {challenge.content.conceptos.map((concept) => {
                        const paired = associationPairs.some((pair) => pair.concepto === concept)
                        return (
                          <button
                            key={concept}
                            type="button"
                            disabled={Boolean(result)}
                            onClick={() => selectConcept(concept)}
                            className={`block w-full rounded-lg border p-3 text-left ${
                              selectedConcept === concept ? 'border-blue-500 bg-blue-50' : 'border-gray-200'
                            } ${paired ? 'opacity-60' : ''}`}
                          >
                            {concept}
                            {paired && <span className="float-right text-xs text-green-700">Asociado</span>}
                          </button>
                        )
                      })}
                    </div>
                    <div className="space-y-2">
                      <h4 className="font-bold text-gray-700">Explicaciones</h4>
                      {challenge.content.explicaciones.map((explanation) => {
                        const paired = associationPairs.some((pair) => pair.explicacion === explanation)
                        return (
                          <button
                            key={explanation}
                            type="button"
                            disabled={Boolean(result)}
                            onClick={() => selectExplanation(explanation)}
                            className={`block w-full rounded-lg border p-3 text-left ${
                              selectedExplanation === explanation ? 'border-blue-500 bg-blue-50' : 'border-gray-200'
                            } ${paired ? 'opacity-60' : ''}`}
                          >
                            {explanation}
                            {paired && <span className="float-right text-xs text-green-700">Asociada</span>}
                          </button>
                        )
                      })}
                    </div>
                  </div>
                </>
              )}

              {selectedGame.id === 'detectar_error' && (
                <fieldset className="mt-4 space-y-2">
                  <legend className="mb-2 font-bold text-gray-700">Selecciona la línea incorrecta</legend>
                  {challenge.content.codigo.map((line) => (
                    <label
                      key={line.linea}
                      className={`flex cursor-pointer items-start gap-3 rounded-lg border p-3 font-mono ${
                        selectedLine === line.linea ? 'border-blue-500 bg-blue-50' : 'border-gray-200'
                      }`}
                    >
                      <input
                        type="radio"
                        name="provided-error-line"
                        value={line.linea}
                        checked={selectedLine === line.linea}
                        disabled={Boolean(result)}
                        onChange={() => setSelectedLine(line.linea)}
                      />
                      <code className="whitespace-pre-wrap">{line.linea}</code>
                    </label>
                  ))}
                </fieldset>
              )}

              {selectedGame.id === 'ordenar_codigo' && (
                <>
                  <p className="mt-4 text-sm text-gray-600">
                    Usa las flechas para colocar los bloques en el orden correcto.
                  </p>
                  <ol className="mt-3 space-y-2">
                    {orderedIds.map((blockId, index) => {
                      const block = challenge.content.bloques.find((item) => item.id === blockId)
                      return (
                        <li key={blockId} className="flex items-center gap-3 rounded-lg border border-gray-200 p-3">
                          <code className="flex-1 whitespace-pre-wrap">{block.linea}</code>
                          <button
                            type="button"
                            aria-label={`Subir bloque ${index + 1}`}
                            disabled={Boolean(result) || index === 0}
                            onClick={() => moveBlock(index, -1)}
                            className="rounded bg-gray-100 px-3 py-1 disabled:opacity-40"
                          >
                            ↑
                          </button>
                          <button
                            type="button"
                            aria-label={`Bajar bloque ${index + 1}`}
                            disabled={Boolean(result) || index === orderedIds.length - 1}
                            onClick={() => moveBlock(index, 1)}
                            className="rounded bg-gray-100 px-3 py-1 disabled:opacity-40"
                          >
                            ↓
                          </button>
                        </li>
                      )
                    })}
                  </ol>
                </>
              )}

              {!result ? (
                <button
                  type="button"
                  onClick={submitAnswer}
                  disabled={!answerIsReady() || isSubmitting}
                  className="mt-5 rounded-full bg-blue-600 px-6 py-3 font-bold text-white disabled:opacity-50"
                >
                  {isSubmitting ? 'Comprobando…' : 'Comprobar'}
                </button>
              ) : (
                <div role="status" className="mt-5 rounded-lg border border-gray-200 bg-gray-50 p-4">
                  <h4 className={`font-bold ${result.correct ? 'text-green-700' : 'text-red-700'}`}>
                    {result.correct ? '¡Correcto!' : 'No es correcto'}
                  </h4>
                  {!result.correct && (
                    <div className="mt-2 text-sm text-gray-700">
                      {result.explanation && <p>{result.explanation}</p>}
                      {selectedGame.id === 'asociar_conceptos' && (
                        <ul className="mt-2 list-inside list-disc">
                          {result.solution.asociaciones.map((pair) => (
                            <li key={pair.concepto}>{pair.concepto} — {pair.explicacion}</li>
                          ))}
                        </ul>
                      )}
                      {selectedGame.id === 'detectar_error' && (
                        <p className="mt-2">
                          Línea correcta: {result.solution.selected_line}
                        </p>
                      )}
                      {selectedGame.id === 'ordenar_codigo' && (
                        <ol className="mt-2 list-inside list-decimal">
                          {result.solution.ordered_ids.map((blockId) => (
                            <li key={blockId}>{challenge.content.bloques.find((block) => block.id === blockId)?.linea}</li>
                          ))}
                        </ol>
                      )}
                    </div>
                  )}
                  {result.correct && result.explanation && <p className="mt-2 text-sm text-gray-700">{result.explanation}</p>}
                  <button
                    type="button"
                    onClick={loadChallenge}
                    disabled={isLoading}
                    className="mt-4 rounded-full bg-gray-800 px-5 py-2 font-bold text-white disabled:opacity-50"
                  >
                    {isLoading ? 'Cargando…' : 'Siguiente prueba'}
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </section>
  )
}

export default ProvidedGamesPractice
