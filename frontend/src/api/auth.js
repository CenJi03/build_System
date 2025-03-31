import axios from './axios'

export const authApi = {
  async register(userData) {
    const response = await axios.post('/auth/register/', userData)
    return response.data
  },

  async login(credentials) {
    const response = await axios.post('/auth/login/', credentials)
    return response.data
  },

  async refreshToken(refreshToken) {
    const response = await axios.post('/auth/token/refresh/', { 
      refresh: refreshToken 
    })
    return response.data
  },

  async getUserProfile() {
    const response = await axios.get('/auth/profile/')
    return response.data
  },

  async updateUserProfile(profileData) {
    const response = await axios.patch('/auth/profile/', profileData)
    return response.data
  }
}