const API_BASE = import.meta.env.VITE_TRAINING_API_URL || 'http://localhost:8000/api/training'

export async function getTrainingOverview() {
  const response = await fetch(`${API_BASE}/`, { credentials: 'include' })
  if (!response.ok) throw new Error(`Training overview failed: ${response.status}`)
  return response.json()
}
