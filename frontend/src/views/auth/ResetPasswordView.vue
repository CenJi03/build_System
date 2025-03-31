<template>
  <div class="reset-password-page">
    <base-card title="Reset Password" class="reset-password-card">
      <template v-if="isLoading">
        <div class="loading-state">
          <p>Processing your request...</p>
        </div>
      </template>
      
      <template v-else-if="isSuccess">
        <div class="success-state">
          <div class="icon-container">
            <span class="success-icon">✓</span>
          </div>
          <h2>Password Reset Successful</h2>
          <p>Your password has been successfully reset.</p>
          <base-button 
            variant="primary" 
            @click="goToLogin" 
            full-width
          >
            Continue to Login
          </base-button>
        </div>
      </template>
      
      <template v-else-if="!token">
        <div class="request-form">
          <p>Enter your email address to receive a password reset link.</p>
          
          <form @submit.prevent="requestReset">
            <div class="form-group">
              <base-input
                id="email"
                label="Email"
                type="email"
                v-model="email"
                :error="emailError"
                :disabled="requestSubmitting"
                placeholder="Enter your email"
                required
              />
            </div>
            
            <base-button 
              type="submit" 
              variant="primary" 
              :disabled="requestSubmitting"
              full-width
            >
              {{ requestSubmitting ? 'Sending...' : 'Send Reset Link' }}
            </base-button>
          </form>
          
          <p v-if="requestSuccess" class="success-message">
            Password reset link has been sent to your email.
          </p>
          
          <p v-if="requestError" class="error-message">
            {{ requestError }}
          </p>
        </div>
      </template>
      
      <template v-else>
        <div class="reset-form">
          <p>Enter your new password below.</p>
          
          <form @submit.prevent="resetPassword">
            <div class="form-group">
              <base-input
                id="password"
                label="New Password"
                type="password"
                v-model="newPassword"
                :error="passwordError"
                :disabled="resetSubmitting"
                placeholder="Enter new password"
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
                :disabled="resetSubmitting"
                placeholder="Confirm new password"
                required
              />
            </div>
            
            <base-button 
              type="submit" 
              variant="primary" 
              :disabled="resetSubmitting"
              full-width
            >
              {{ resetSubmitting ? 'Resetting...' : 'Reset Password' }}
            </base-button>
          </form>
          
          <p v-if="resetError" class="error-message">
            {{ resetError }}
          </p>
        </div>
      </template>
      
      <div class="back-to-login">
        <router-link to="/login">Back to Login</router-link>
      </div>
    </base-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { validators, validate } from '@/utils/validators'
import BaseCard from '@/components/UI/BaseCard.vue'
import BaseButton from '@/components/UI/BaseButton.vue'
import BaseInput from '@/components/UI/BaseInput.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

// Shared state
const isLoading = ref(false)
const isSuccess = ref(false)
const token = ref(route.query.token)

// Password reset request form
const email = ref('')
const emailError = ref('')
const requestSubmitting = ref(false)
const requestSuccess = ref(false)
const requestError = ref('')

// Password reset form
const newPassword = ref('')
const confirmPassword = ref('')
const passwordError = ref('')
const confirmPasswordError = ref('')
const resetSubmitting = ref(false)
const resetError = ref('')

async function requestReset() {
  emailError.value = ''
  requestError.value = ''
  
  // Validate email
  const emailValidation = validate(email.value, validators.required, validators.email)
  if (emailValidation !== true) {
    emailError.value = emailValidation
    return
  }
  
  requestSubmitting.value = true
  
  try {
    await authStore.requestPasswordReset(email.value)
    requestSuccess.value = true
    email.value = ''
  } catch (error) {
    requestError.value = error.response?.data?.detail || 'Failed to send reset link. Please try again.'
  } finally {
    requestSubmitting.value = false
  }
}

async function resetPassword() {
  passwordError.value = ''
  confirmPasswordError.value = ''
  resetError.value = ''
  
  // Validate password
  const passwordValidation = validate(
    newPassword.value, 
    validators.required, 
    validators.passwordStrength
  )
  if (passwordValidation !== true) {
    passwordError.value = passwordValidation
    return
  }
  
  // Validate password confirmation
  if (newPassword.value !== confirmPassword.value) {
    confirmPasswordError.value = 'Passwords do not match'
    return
  }
  
  isLoading.value = true
  resetSubmitting.value = true
  
  try {
    await authStore.resetPassword(token.value, newPassword.value)
    isSuccess.value = true
  } catch (error) {
    resetError.value = error.response?.data?.detail || 'Password reset failed. The link may have expired.'
  } finally {
    isLoading.value = false
    resetSubmitting.value = false
  }
}

function goToLogin() {
  router.push('/login')
}
</script>

<style scoped>
.reset-password-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f0f2f5;
  padding: 2rem;
}

.reset-password-card {
  width: 100%;
  max-width: 400px;
}

.loading-state,
.success-state {
  text-align: center;
  padding: 1rem;
}

.icon-container {
  margin-bottom: 1rem;
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

.form-group {
  margin-bottom: 1.5rem;
}

.back-to-login {
  margin-top: 1.5rem;
  text-align: center;
}

.back-to-login a {
  color: #007bff;
  text-decoration: none;
}

.back-to-login a:hover {
  text-decoration: underline;
}

.success-message {
  color: #28a745;
  margin-top: 1rem;
  text-align: center;
}

.error-message {
  color: #dc3545;
  margin-top: 1rem;
  text-align: center;
}

h2 {
  margin-bottom: 1rem;
}

p {
  margin-bottom: 1.5rem;
  color: #666;
}
</style>
