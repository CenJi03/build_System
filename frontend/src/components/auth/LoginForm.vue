<template>
  <form @submit.prevent="handleLogin" class="login-form">
    <div class="form-group">
      <base-input
        id="email"
        label="Email or Username"
        v-model="loginIdentifier"
        :error="loginIdentifierError"
        :disabled="isLoading"
        placeholder="Enter your email or username"
        required
      />
    </div>

    <div class="form-group">
      <base-input
        id="password"
        label="Password"
        type="password"
        v-model="password"
        :error="passwordError"
        :disabled="isLoading"
        placeholder="Enter your password"
        required
      />
    </div>

    <base-button 
      type="submit" 
      :disabled="isLoading"
      variant="primary"
      class="submit-btn"
    >
      {{ isLoading ? 'Logging in...' : 'Login' }}
    </base-button>

    <p v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </p>

    <p class="signup-link">
      Don't have an account? 
      <router-link to="/register">Register here</router-link>
    </p>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { validators, validate } from '@/utils/validators'
import BaseInput from '@/components/UI/BaseInput.vue'
import BaseButton from '@/components/UI/BaseButton.vue'

// State variables
const loginIdentifier = ref('')
const password = ref('')
const errorMessage = ref('')
const isLoading = ref(false)

// Error state for specific fields
const loginIdentifierError = ref('')
const passwordError = ref('')

// Auth store and router
const authStore = useAuthStore()
const router = useRouter()

// Login handler
async function handleLogin() {
  // Reset previous errors
  loginIdentifierError.value = ''
  passwordError.value = ''
  errorMessage.value = ''

  // Validate login identifier
  const loginIdentifierValidation = validate(
    loginIdentifier.value,
    validators.required
  )
  if (loginIdentifierValidation !== true) {
    loginIdentifierError.value = loginIdentifierValidation
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
    await authStore.login({
      email: loginIdentifier.value, // We're using email field but sending username or email
      password: password.value
    })
  } catch (error) {
    // Handle login errors
    errorMessage.value = error.response?.data?.detail || error.response?.data?.error 
      || 'Login failed. Please check your credentials.'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.login-form {
  width: 100%;
}

.submit-btn {
  width: 100%;
  margin-top: 1rem;
}

.error-message {
  color: #dc3545;
  text-align: center;
  margin-top: 1rem;
}

.signup-link {
  text-align: center;
  margin-top: 1.5rem;
}

.signup-link a {
  color: #007bff;
  text-decoration: none;
  font-weight: 500;
}

.signup-link a:hover {
  text-decoration: underline;
}
</style>
