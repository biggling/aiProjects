import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE_URL || ''

const client = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add auth header
client.interceptors.request.use((config) => {
  const apiKey = import.meta.env.VITE_API_KEY || localStorage.getItem('api_key') || ''
  if (apiKey) {
    config.headers.Authorization = `Bearer ${apiKey}`
  }
  return config
})

export default client
