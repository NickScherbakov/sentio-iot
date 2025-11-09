import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add auth token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Auth API
export const authAPI = {
  login: (username, password) =>
    api.post('/auth/login', { username, password }),
}

// Metrics API
export const metricsAPI = {
  query: (query, start, end, step) =>
    api.post('/metrics/query', { query, start, end, step }),
  listSeries: () => api.get('/metrics/series'),
}

// Logs API
export const logsAPI = {
  query: (query, start, end, limit) =>
    api.post('/logs/query', { query, start, end, limit }),
  listLabels: () => api.get('/logs/labels'),
}

// Traces API
export const tracesAPI = {
  query: (params) => api.post('/traces/query', params),
  getTrace: (traceId) => api.get(`/traces/${traceId}`),
}

// Devices API
export const devicesAPI = {
  list: () => api.get('/devices'),
  get: (id) => api.get(`/devices/${id}`),
  create: (device) => api.post('/devices', device),
  update: (id, device) => api.put(`/devices/${id}`, device),
  delete: (id) => api.delete(`/devices/${id}`),
}

// Alerts API
export const alertsAPI = {
  list: () => api.get('/alerts'),
  get: (id) => api.get(`/alerts/${id}`),
  create: (alert) => api.post('/alerts', alert),
  update: (id, alert) => api.put(`/alerts/${id}`, alert),
  delete: (id) => api.delete(`/alerts/${id}`),
}

// AI API
export const aiAPI = {
  getAnomalies: () => api.get('/ai/anomalies'),
  getPredictions: () => api.get('/ai/predictions'),
}

// Status API
export const statusAPI = {
  get: () => api.get('/status'),
}

export default api
