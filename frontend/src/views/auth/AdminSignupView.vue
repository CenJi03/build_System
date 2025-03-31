<template>
  <div class="admin-signup-page">
    <div class="admin-signup-container">
      <h2>Create Admin Account</h2>
      
      <div v-if="isSuccess" class="success-container">
        <div class="success-icon">✓</div>
        <h3>Admin Account Created!</h3>
        <p>
          The admin account has been successfully created.
        </p>
        <base-button
          @click="goToDashboard"
          variant="primary"
          class="action-btn"
        >
          Go to Dashboard
        </base-button>
      </div>
      
      <form v-else @submit.prevent="handleAdminSignup" class="admin-signup-form">
        <div class="form-group">
          <base-input
            id="username"
            label="Username"
            v-model="username"
            :error="usernameError"
            :disabled="isLoading"
            placeholder="Enter admin username"
            required
          />
        </div>
        
        <div class="form-group">
          <base-input
            id="email"
            label="Email"
            type="email"
            v-model="email"
            :error="emailError"
            :disabled="isLoading"
            placeholder="Enter admin email"
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
            placeholder="Create a strong password"
            required
          />
        </div>
        
        <div class="form-group">
          <base-input
            id="confirmPassword"
            label="Confirm Password"
            type="password"
            v-model="confirmPassword"
            :error="confirmPasswordError"
            :disabled="isLoading"
            placeholder="Confirm password"
            required
          />
        </div>
        
        <base-button
          type="submit"
          :disabled="isLoading"
          variant="primary"
          class="submit-btn"
        >
          {{ isLoading ? 'Creating Admin...' : 'Create Admin Account' }}
        </base-button>
        
        <p v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { validators, validate } from '@/utils/validators'
import BaseInput from '@/components/UI/BaseInput.vue'
import BaseButton from '@/components/UI/BaseButton.vue'

// State variables
const username = ref('')
const email = ref('r2003kamsan@gmail.com') // Pre-filled from parameters
const password = ref('November#09')        // Pre-filled from parameters
const confirmPassword = ref('November#09') // Pre-filled from parameters
const errorMessage = ref('')
const isLoading = ref(false)
const isSuccess = ref(false)

// Error state for specific fields
const usernameError = ref('')
const emailError = ref('')
const passwordError = ref('')
const confirmPasswordError = ref('')

// Router and auth store
const router = useRouter()
const authStore = useAuthStore()

// Admin signup handler
async function handleAdminSignup() {
  // Reset previous errors
  usernameError.value = ''
  emailError.value = ''
  passwordError.value = ''
  confirmPasswordError.value = ''
  errorMessage.value = ''

  // Validate username
  const usernameValidation = validate(
    username.value, 
    validators.required,
    validators.minLength(3),
    validators.maxLength(20)
  )
  if (usernameValidation !== true) {
    usernameError.value = usernameValidation
    return
  }

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
    validators.required,
    validators.passwordStrength
  )
  if (passwordValidation !== true) {
    passwordError.value = passwordValidation
    return
  }

  // Validate password confirmation
  if (password.value !== confirmPassword.value) {
    confirmPasswordError.value = 'Passwords do not match'
    return
  }

  try {
    isLoading.value = true
    await authStore.createAdminAccount({
      username: username.value,
      email: email.value,
      password: password.value
    })
    isSuccess.value = true
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Failed to create admin account'
  } finally {
    isLoading.value = false
  }
}

// Navigate to dashboard
function goToDashboard() {
  router.push('/dashboard')
}
</script>

<style scoped>
.admin-signup-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f0f2f5;
  padding: 2rem;
}

.admin-signup-container {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  width: 100%;
  max-width: 500px;
}

h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #333;
}

.submit-btn, .action-btn {
  width: 100%;
  margin-top: 1rem;
}

.error-message {
  color: #dc3545;
  text-align: center;
  margin-top: 1rem;
}

.success-container {
  text-align: center;
  padding: 1rem;
}

.success-icon {
  display: inline-flex;
  justify-content: center;
  align-items: center;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  font-size: 2rem;
  background-color: #28a745;
  color: white;
  margin-bottom: 1rem;
}

h3 {
  margin-bottom: 1rem;
}
</style>
