<template>
  <div class="login-page">
    <div class="login-container">
      <h2>Login to Your Account</h2>
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="email">Email</label>
          <input 
            type="email" 
            id="email" 
            v-model="email" 
            required 
            placeholder="Enter your email"
          />
          <span v-if="emailError" class="error">{{ emailError }}</span>
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <div class="password-input-container">
            <input 
              :type="showPassword ? 'text' : 'password'" 
              id="password" 
              v-model="password" 
              required 
              placeholder="Enter your password"
            />
            <button 
              type="button" 
              class="toggle-password" 
              @mousedown.prevent="showPassword = true"
              @mouseup.prevent="showPassword = false"
              @mouseleave="showPassword = false"
              title="Hold to show password"
            >
              <svg v-if="showPassword" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="eye-icon">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                <circle cx="12" cy="12" r="3"></circle>
                <line x1="1" y1="1" x2="23" y2="23"></line>
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="eye-icon">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                <circle cx="12" cy="12" r="3"></circle>
              </svg>
            </button>
          </div>
          <span v-if="passwordError" class="error">{{ passwordError }}</span>
        </div>

        <div class="forgot-password">
          <router-link to="/reset-password">Forgot password?</router-link>
        </div>

        <button type="submit" :disabled="isLoading">
          {{ isLoading ? 'Logging in...' : 'Login' }}
        </button>

        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
          <div v-if="showDebugInfo" class="debug-info">
            <small>{{ debugInfo }}</small>
          </div>
        </div>

        <p class="system-note">
          Contact system administrator for account creation
        </p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { validators, validate } from '@/utils/validators'

// State variables
const email = ref('')
const password = ref('')
const errorMessage = ref('')
const isLoading = ref(false)
const debugInfo = ref('')
const showDebugInfo = ref(false)
const showPassword = ref(false)

// Error state for specific fields
const emailError = ref('')
const passwordError = ref('')

// Auth store and router
const authStore = useAuthStore()
const router = useRouter()

// Check if already authenticated
onMounted(() => {
  if (authStore.isAuthenticated) {
    router.push('/dashboard')
  }
  
  // Debug mode toggle - remove in production
  window.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.shiftKey && e.key === 'D') {
      showDebugInfo.value = !showDebugInfo.value
    }
  })
})

// Login handler
async function handleLogin() {
  // Reset previous errors
  emailError.value = ''
  passwordError.value = ''
  errorMessage.value = ''
  debugInfo.value = ''

  // Validate email
  const emailValidation = validate(
    email.value, 
    validators.required,
    validators.email
  )
  if (emailValidation !== true) {
    emailError.value = emailValidation
    return
  }

  // Validate password
  const passwordValidation = validate(
    password.value, 
    validators.required
  )
  if (passwordValidation !== true) {
    passwordError.value = passwordValidation
    return
  }

  try {
    isLoading.value = true
    console.log('Login attempt with credentials:', { 
      email: email.value, 
      passwordLength: password.value.length 
    })
    
    const response = await authStore.login({
      email: email.value,
      password: password.value
    })
    
    console.log('Login response:', response)
    // Successfully logged in, router.push is handled in the store
  } catch (error) {
    console.error('Full login error:', {
      response: error.response,
      status: error.response?.status,
      data: error.response?.data,
      message: error.message
    })
    
    errorMessage.value = error.response?.data?.detail 
      || error.response?.data?.error
      || 'Login failed. Please check your credentials.'
      
    // Add debugging info
    debugInfo.value = `Status: ${error.response?.status || 'N/A'}, Code: ${error.code || 'Unknown'}`
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f0f2f5;
}

.login-container {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  width: 100%;
  max-width: 400px;
}

h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #333;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

button {
  width: 100%;
  padding: 0.75rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  margin-top: 1rem;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.error {
  color: #dc3545;
  font-size: 0.8rem;
  margin-top: 0.5rem;
}

.error-message {
  color: #dc3545;
  text-align: center;
  margin-top: 1rem;
}

.system-note {
  text-align: center;
  margin-top: 1.5rem;
  color: #666;
  font-size: 0.9rem;
}

.forgot-password {
  text-align: right;
  margin-bottom: 1rem;
}

.forgot-password a {
  color: #007bff;
  text-decoration: none;
  font-size: 0.9rem;
}

.forgot-password a:hover {
  text-decoration: underline;
}

.password-input-container {
  position: relative;
  display: flex;
  align-items: center;
}

.password-input-container input {
  flex-grow: 1;
  padding-right: 40px; /* Make space for the toggle button */
}

.toggle-password {
  position: absolute;
  right: 10px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  height: 100%;
  margin: 0;
  width: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #666;
  font-size: 1rem;
}

.toggle-password:hover {
  color: #333;
}

.toggle-password:focus {
  outline: none;
}

.eye-icon {
  color: #666;
}

.debug-info {
  font-size: 0.75rem;
  color: #999;
  margin-top: 0.25rem;
  background-color: #f8f8f8;
  padding: 0.25rem;
  border-radius: 3px;
}
</style>