import { useCallback, useEffect, useState } from 'react'
import Login from './components/auth/Login'
import DailyCycleView from './components/training/DailyCycleView'
import {
  getTrainingHistory,
  getTrainingOverview,
  getTrainingProgress,
  submitTrainingAnswer,
} from './services/trainingApi'
import { clearTokens, hasStoredTokens } from './services/authApi'

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(hasStoredTokens)
  const [data, setData] = useState(null)
  const [progress, setProgress] = useState(null)
  const [history, setHistory] = useState([])
  const [error, setError] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  const refreshTraining = useCallback(async () => {
    setIsLoading(true)
    setError(null)
    try {
      const overview = await getTrainingOverview()
      const [currentProgress, currentHistory] = await Promise.all([
        getTrainingProgress(),
        getTrainingHistory(),
      ])
      setData(overview)
      setProgress(currentProgress)
      setHistory(currentHistory.results)
    } catch (requestError) {
      setError(requestError.message)
      if (!hasStoredTokens()) {
        clearTokens()
        setIsAuthenticated(false)
      }
    } finally {
      setIsLoading(false)
    }
  }, [])

  useEffect(() => {
    if (isAuthenticated) refreshTraining()
  }, [isAuthenticated, refreshTraining])

  const handleExerciseSubmit = async (exerciseNumber, answer) => {
    try {
      const result = await submitTrainingAnswer(exerciseNumber, answer)
      await refreshTraining()
      return result
    } catch (requestError) {
      if (!hasStoredTokens()) setIsAuthenticated(false)
      throw requestError
    }
  }

  if (!isAuthenticated) {
    return <Login onLoginSuccess={() => setIsAuthenticated(true)} />
  }

  if (isLoading && !data) {
    return (
      <main className="min-h-screen flex items-center justify-center bg-gray-50">
        <p className="text-gray-600">Cargando ciclo diario…</p>
      </main>
    )
  }

  if (error && !data) {
    return (
      <main className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-red-500 mb-2">DuckyTraining</h1>
          <p className="text-gray-600">{error}</p>
          <button className="mt-4 underline" onClick={refreshTraining}>Reintentar</button>
        </div>
      </main>
    )
  }

  return (
    <>
      {error && <p role="alert" className="bg-red-100 text-red-800 p-3 text-center">{error}</p>}
      {data && (
        <DailyCycleView
          data={data}
          progress={progress}
          history={history}
          onRefresh={refreshTraining}
          onExerciseSubmit={handleExerciseSubmit}
        />
      )}
    </>
  )
}
