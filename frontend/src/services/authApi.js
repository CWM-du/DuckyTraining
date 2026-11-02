const trainingApiUrl = import.meta.env.VITE_TRAINING_API_URL
const API_ROOT = (
  import.meta.env.VITE_API_BASE_URL
  || (trainingApiUrl ? trainingApiUrl.replace(/\/training\/?$/, '') : 'http://localhost:8000/api')
).replace(/\/$/, '')
const ACCESS_TOKEN_KEY = 'ducky_training_access_token'
const REFRESH_TOKEN_KEY = 'ducky_training_refresh_token'

let refreshInProgress = null

export async function obtainTokens(username, password) {
  const response = await fetch(`${API_ROOT}/token/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  })
  const data = await response.json()
  if (!response.ok) {
    throw new Error(data.detail || 'Usuario o contraseña incorrectos.')
  }

  sessionStorage.setItem(ACCESS_TOKEN_KEY, data.access)
  sessionStorage.setItem(REFRESH_TOKEN_KEY, data.refresh)
  return data
}

export function getAccessToken() {
  return sessionStorage.getItem(ACCESS_TOKEN_KEY)
}

export function clearTokens() {
  sessionStorage.removeItem(ACCESS_TOKEN_KEY)
  sessionStorage.removeItem(REFRESH_TOKEN_KEY)
}

export function refreshAccessToken() {
  if (refreshInProgress) return refreshInProgress

  refreshInProgress = (async () => {
    const refresh = sessionStorage.getItem(REFRESH_TOKEN_KEY)
    if (!refresh) {
      clearTokens()
      return null
    }

    try {
      const response = await fetch(`${API_ROOT}/token/refresh/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh }),
      })
      const data = await response.json()
      if (!response.ok || !data.access) {
        clearTokens()
        return null
      }

      sessionStorage.setItem(ACCESS_TOKEN_KEY, data.access)
      return data.access
    } finally {
      refreshInProgress = null
    }
  })()

  return refreshInProgress
}

export function hasStoredTokens() {
  return Boolean(getAccessToken())
}
