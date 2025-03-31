import { defineStore } from 'pinia'
import { authApi } from '../api/auth'
import { ref } from 'vue'
import router from '../router'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const accessToken = ref(localStorage.getItem('access_token'))
  const refreshToken = ref(localStorage.getItem('refresh_token'))
  const isAuthenticated = ref(!!accessToken.value)
  const loginError = ref(null) // Add error tracking

  async function login(credentials) {
    try {
      console.log('Login attempt with:', { email: credentials.email }) // Log login attempt (no password)
      loginError.value = null // Reset previous errors
      
      const response = await authApi.login(credentials)
      console.log('Login response:', { success: !!response, hasUser: !!response.user, hasTokens: !!(response.access && response.refresh) }) 
      
      // Check if we have all required data before proceeding
      if (!response.access || !response.refresh) {
        throw new Error('Invalid response: Missing access or refresh tokens')
      }

      setTokens(response.access, response.refresh)
      user.value = response.user || await fetchUserProfile() // Fallback to fetching profile if not included
      
      // Ensure we navigate to dashboard after successful login
      router.push('/dashboard')
      return response
    } catch (error) {
      console.error('Login failed', error)
      loginError.value = error.response?.data?.detail || 'Authentication failed. Please check your credentials.'
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

  // Enhance token refresh to handle multiple calls
  let refreshPromise = null
  async function refreshAccessToken() {
    // If a refresh is already in progress, return that promise
    if (refreshPromise) return refreshPromise
    
    try {
      refreshPromise = authApi.refreshToken(refreshToken.value)
      const response = await refreshPromise
      setTokens(response.access, refreshToken.value)
      return response.access
    } catch (error) {
      logout()
      throw error
    } finally {
      refreshPromise = null
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

  async function register(userData) {
    try {
      const response = await authApi.register(userData)
      router.push('/verify-email')
      return response
    } catch (error) {
      console.error('Registration failed', error)
      throw error
    }
  }

  async function verifyEmail(token) {
    try {
      const response = await authApi.verifyEmail(token)
      router.push('/login')
      return response
    } catch (error) {
      console.error('Email verification failed', error)
      throw error
    }
  }

  async function requestPasswordReset(email) {
    try {
      return await authApi.requestPasswordReset(email)
    } catch (error) {
      console.error('Password reset request failed', error)
      throw error
    }
  }

  async function resetPassword(token, newPassword) {
    try {
      const response = await authApi.resetPassword(token, newPassword)
      router.push('/login')
      return response
    } catch (error) {
      console.error('Password reset failed', error)
      throw error
    }
  }

  async function setup2FA() {
    try {
      return await authApi.setup2FA()
    } catch (error) {
      console.error('2FA setup failed', error)
      throw error
    }
  }

  async function verify2FA(code) {
    try {
      return await authApi.verify2FA(code)
    } catch (error) {
      console.error('2FA verification failed', error)
      throw error
    }
  }

  async function deleteAccount(password) {
    try {
      const response = await authApi.deleteAccount(password)
      logout()
      router.push('/account-deleted')
      return response
    } catch (error) {
      console.error('Account deletion failed', error)
      throw error
    }
  }

  async function createAdminAccount(adminData) {
    try {
      const response = await authApi.createAdminAccount(adminData)
      return response
    } catch (error) {
      console.error('Admin account creation failed', error)
      throw error
    }
  }

  return {
    user,
    accessToken,
    refreshToken,
    isAuthenticated,
    loginError, // Expose the login error
    login,
    logout,
    fetchUserProfile,
    updateUserProfile,
    refreshAccessToken,
    register,
    verifyEmail,
    requestPasswordReset,
    resetPassword,
    setup2FA,
    verify2FA,
    deleteAccount,
    createAdminAccount
  }
})