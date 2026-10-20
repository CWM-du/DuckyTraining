import {
  clearTokens,
  getAccessToken,
  refreshAccessToken,
} from './authApi'

const API_BASE = import.meta.env.VITE_TRAINING_API_URL
  || `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'}/training`

async function request(path, options = {}) {
  const send = (token) => {
    const headers = new Headers(options.headers)
    headers.set('Content-Type', 'application/json')
    if (token) headers.set('Authorization', ['Bearer', token].join(' '))
    return fetch(`${API_BASE}${path}`, { ...options, headers })
  }

  let response = await send(getAccessToken())
  if (response.status === 401) {
    const refreshedToken = await refreshAccessToken()
    if (refreshedToken) {
      response = await send(refreshedToken)
    }
    if (response.status === 401) {
      clearTokens()
    }
  }

  const data = await response.json()
  if (!response.ok) {
    throw new Error(data.message || data.detail || `Training request failed: ${response.status}`)
  }
  return data
}

export function getTrainingOverview() {
  return request('/')
}

export function getTrainingProgress() {
  return request('/progress/')
}

export function getTrainingHistory(limit = 20) {
  return request(`/history/?limit=${limit}`)
}

export function submitTrainingAnswer(exerciseNumber, answer) {
  return request(`/exercises/${exerciseNumber}/submit/`, {
    method: 'POST',
    body: JSON.stringify({ answer }),
  })
}
