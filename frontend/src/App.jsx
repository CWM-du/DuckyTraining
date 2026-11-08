import { useEffect, useState } from 'react'
import DailyCycleView from './components/training/DailyCycleView'
import Login from './components/auth/Login'
import axios from 'axios'

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)

  // Cuando el usuario se loguea con éxito, el backend ya nos dio el token
  // y ahora sí activamos la llamada real a Django
  useEffect(() => {
    if (isAuthenticated) {
      const fetchRealTrainingData = async () => {
        try {
          const token = localStorage.getItem('access'); // O de donde lo guarde tu componente Login
          
          // PRO-TIP: En producción, cambia esta URL por una variable de entorno.
          // Ej: const baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
          const response = await axios.get('http://localhost:8000/api/training/', {
            headers: {
              Authorization: `Bearer ${token}`
            }
          });

          setData(response.data);
        } catch (err) {
          console.error("Error conectando con el backend:", err);
          setError(err.response?.data?.detail || err.message);
        }
      };

      fetchRealTrainingData();
    }
  }, [isAuthenticated]);

  // --- 1º BARRERA: SEGURIDAD (LOGIN) ---
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

  // --- 3º BARRERA: ESPERANDO DATOS DEL BACKEND ---
  if (!data) {
    return (
      <main className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-blue-600 mb-4">DuckyTraining</h1>
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="text-gray-500 mt-4">Conectando con el servidor...</p>
        </div>
      </main>
    )
  }

  // --- ÉXITO: MOSTRAR LOS DATOS REALES DE DJANGO ---
  return <DailyCycleView data={data} />
}