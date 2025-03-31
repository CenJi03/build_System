import axios from './axios'

export const authApi = {
  async login(credentials) {
    try {
      const response = await axios.post('/auth/token/', credentials)
      return response.data
    } catch (error) {
      console.error('Login failed', error.response?.data)
      throw error
    }
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
  },

  async register(userData) {
    const response = await axios.post('/auth/register/', userData)
    return response.data
  },

  async verifyEmail(token) {
    const response = await axios.post('/auth/verify-email/', { token })
    return response.data
  },

  async requestPasswordReset(email) {
    const response = await axios.post('/auth/reset-password-request/', { email })
    return response.data
  },
  
  async resetPassword(token, newPassword) {
    const response = await axios.post('/auth/reset-password-confirm/', {
      token,
      new_password: newPassword
    })
    return response.data
  },

  async setup2FA() {
    const response = await axios.post('/auth/setup-2fa/')
    return response.data
  },

  async verify2FA(token) {
    const response = await axios.post('/auth/verify-2fa/', { token })
    return response.data
  },

  async disable2FA(token, password) {
    const response = await axios.post('/auth/disable-2fa/', { 
      token,
      password 
    })
    return response.data
  },

  async deleteAccount(password) {
    const response = await axios.post('/auth/delete-account/', { password })
    return response.data
  },

  async createAdminAccount(adminData) {
    const response = await axios.post('/auth/create-admin/', adminData)
    return response.data
  }
}