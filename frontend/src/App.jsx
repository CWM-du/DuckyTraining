import { useEffect, useState } from 'react'
import { getTrainingOverview } from './services/trainingApi'
import DailyCycleView from './components/training/DailyCycleView' 

export default function App() {
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    getTrainingOverview().then(setData).catch((e) => setError(e.message))
  }, [])

  if (error) {
    return (
      <main className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-red-500 mb-2">DuckyTraining</h1>
          <p className="text-gray-600">No se pudo cargar Training: {error}</p>
        </div>
      </main>
    )
  }

  if (!data) {
    return (
      <main className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-blue-600 mb-4">DuckyTraining</h1>
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="text-gray-500 mt-4">Cargando ciclo diario…</p>
        </div>
      </main>
    )
  }

  // Aquí ocurre la magia: Le pasamos los datos reales al componente visual
  return <DailyCycleView data={data} />
}