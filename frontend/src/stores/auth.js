import { defineStore } from 'pinia'
import { authApi } from '../api/auth'
import { ref } from 'vue'
import router from '../router'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const accessToken = ref(localStorage.getItem('access_token'))
  const refreshToken = ref(localStorage.getItem('refresh_token'))
  const isAuthenticated = ref(!!accessToken.value)

  async function register(userData) {
    try {
      const response = await authApi.register(userData)
      setTokens(response.access, response.refresh)
      user.value = response.user
      router.push('/dashboard')
      return response
    } catch (error) {
      console.error('Registration failed', error)
      throw error
    }
  }

  async function login(credentials) {
    try {
      const response = await authApi.login(credentials)
      setTokens(response.access, response.refresh)
      user.value = response.user
      router.push('/dashboard')
      return response
    } catch (error) {
      console.error('Login failed', error)
      throw error
    }
  }

  async function fetchUserProfile() {
    try {
      user.value = await authApi.getUserProfile()
      return user.value
    } catch (error) {
      console.error('Failed to fetch user profile', error)
      logout()
      throw error
    }
  }

  async function updateUserProfile(profileData) {
    try {
      const updatedUser = await authApi.updateUserProfile(profileData)
      user.value = updatedUser
      return updatedUser
    } catch (error) {
      console.error('Failed to update profile', error)
      throw error
    }
  }

  function setTokens(access, refresh) {
    accessToken.value = access
    refreshToken.value = refresh
    isAuthenticated.value = true
    
    // Store tokens in local storage
    localStorage.setItem('access_token', access)
    localStorage.setItem('refresh_token', refresh)
  }

  async function refreshAccessToken() {
    try {
      const response = await authApi.refreshToken(refreshToken.value)
      setTokens(response.access, refreshToken.value)
      return response.access
    } catch (error) {
      logout()
      throw error
    }
  }

  function logout() {
    user.value = null
    accessToken.value = null
    refreshToken.value = null
    isAuthenticated.value = false
    
    // Clear tokens from local storage
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    
    router.push('/login')
  }

  return {
    user,
    accessToken,
    refreshToken,
    isAuthenticated,
    register,
    login,
    logout,
    fetchUserProfile,
    updateUserProfile,
    refreshAccessToken
  }
})