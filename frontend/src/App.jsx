import { useEffect, useState } from 'react'
// 1. Comentamos la API real
// import { getTrainingOverview } from './services/trainingApi'
import DailyCycleView from './components/training/DailyCycleView'
// 2. Importamos nuestros datos de prueba (asegúrate de que la ruta sea correcta)
import mockTrainingData from './data/mockTrainingData' 

import Login from './components/auth/Login'

export default function App() {
  // --- NUEVO ESTADO PARA EL LOGIN ---
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  // 3. Pasamos el mock directamente como estado inicial
  const [data, setData] = useState(mockTrainingData) 
  const [error, setError] = useState(null)

  // 4. Comentamos el useEffect para que no intente hacer la llamada
  /*
  useEffect(() => {
    // Cuando conectemos el backend, esta llamada SOLO debería hacerse 
    // si el usuario está autenticado.
    if (isAuthenticated) {
      getTrainingOverview().then(setData).catch((e) => setError(e.message))
    }
  }, [isAuthenticated])
  */

  // --- 1º BARRERA: SEGURIDAD ---
  // Si no está logueado, cortamos aquí y mostramos el Login.
  if (!isAuthenticated) {
    return <Login onLoginSuccess={() => setIsAuthenticated(true)} />
  }

  // --- 2º BARRERA: ERRORES DE CARGA ---
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

  // --- 3º BARRERA: ESPERANDO DATOS ---
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

  // --- ÉXITO: MOSTRAR JUEGO ---
  return <DailyCycleView data={data} />
}