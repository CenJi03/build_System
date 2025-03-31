import axios from 'axios'
import router from '@/router'
import { useAuthStore } from '@/stores/auth'

// Create axios instance with base URL from environment variable
const instance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

// Add a request interceptor to include JWT token
instance.interceptors.request.use(
  config => {
    const authStore = useAuthStore()
    if (authStore.accessToken) {
      config.headers['Authorization'] = `Bearer ${authStore.accessToken}`
    }
    return config
  },
  error => Promise.reject(error)
)

// Add a response interceptor to handle token refresh
let isRefreshing = false
let failedQueue = []

const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error)
    } else {
      prom.resolve(token)
    }
  })
  failedQueue = []
}

instance.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config
    
    // If error is not 401 or request has already been retried, reject
    if (error.response?.status !== 401 || originalRequest._retry) {
      return Promise.reject(error)
    }
    
    // Set retry flag to avoid infinite loops
    originalRequest._retry = true
    
    // If token refresh is in progress, queue the request
    if (isRefreshing) {
      return new Promise((resolve, reject) => {
        failedQueue.push({ resolve, reject })
      })
        .then(token => {
          originalRequest.headers['Authorization'] = `Bearer ${token}`
          return instance(originalRequest)
        })
        .catch(err => Promise.reject(err))
    }
    
    isRefreshing = true
    
    try {
      const authStore = useAuthStore()
      const newToken = await authStore.refreshAccessToken()
      
      // Update authorization header with new token
      originalRequest.headers['Authorization'] = `Bearer ${newToken}`
      
      // Process the queue with the new token
      processQueue(null, newToken)
      
      return instance(originalRequest)
    } catch (refreshError) {
      // If token refresh fails, redirect to login
      processQueue(refreshError, null)
      router.push('/login')
      return Promise.reject(refreshError)
    } finally {
      isRefreshing = false
    }
  }
)

export default instance