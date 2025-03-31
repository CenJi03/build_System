<template>
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
      <input 
        type="password" 
        id="password" 
        v-model="password" 
        required 
        placeholder="Enter your password"
      />
      <span v-if="passwordError" class="error">{{ passwordError }}</span>
    </div>

    <button type="submit" :disabled="isLoading">
      {{ isLoading ? 'Logging in...' : 'Login' }}
    </button>

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

// State variables
const email = ref('')
const password = ref('')
const errorMessage = ref('')
const isLoading = ref(false)

// Error state for specific fields
const emailError = ref('')
const passwordError = ref('')

// Auth store and router
const authStore = useAuthStore()
const router = useRouter()

// Login handler
async function handleLogin() {
  // Reset previous errors
  emailError.value = ''
  passwordError.value = ''
  errorMessage.value = ''

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
    await authStore.login({
      email: email.value,
      password: password.value
    })
  } catch (error) {
    // Handle login errors
    errorMessage.value = error.response?.data?.detail 
      || 'Login failed. Please check your credentials.'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.login-form {
  max-width: 300px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f7f7f7;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.error {
  color: red;
  font-size: 0.8em;
  margin-top: 5px;
}

.signup-link {
  text-align: center;
  margin-top: 15px;
}

.signup-link a {
  color: #007bff;
  text-decoration: none;
}
</style>