<template>
  <div class="forgot-password-page">
    <div class="forgot-password-container">
      <h2>Reset Your Password</h2>
      
      <div v-if="!emailSent">
        <form @submit.prevent="handleSubmit" class="forgot-password-form">
          <p class="instructions">
            Enter your email address below and we'll send you a link to reset your password.
          </p>
          
          <div class="form-group">
            <base-input
              id="email"
              label="Email"
              type="email"
              v-model="email"
              :error="emailError"
              :disabled="isLoading"
              placeholder="Enter your email address"
              required
            />
          </div>

          <base-button
            type="submit"
            :disabled="isLoading"
            variant="primary"
            class="submit-btn"
          >
            {{ isLoading ? 'Sending...' : 'Send Reset Link' }}
          </base-button>

          <p v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </p>
          
          <p class="login-link">
            Remember your password? <router-link to="/login">Back to login</router-link>
          </p>
        </form>
      </div>

      <div v-else class="success-container">
        <div class="success-icon">✓</div>
        <h3>Reset Link Sent!</h3>
        <p>
          We've sent password reset instructions to <strong>{{ email }}</strong>.
          Please check your email inbox.
        </p>
        <p class="note">
          If you don't see the email within a few minutes, please check your spam folder.
        </p>
        <base-button
          @click="resetForm"
          variant="secondary"
          class="back-btn"
        >
          Back to Reset
        </base-button>
        <router-link to="/login" class="login-link">Return to Login</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { validators, validate } from '@/utils/validators'
import { authApi } from '@/api/auth'
import BaseInput from '@/components/UI/BaseInput.vue'
import BaseButton from '@/components/UI/BaseButton.vue'

// Form state
const email = ref('')
const emailError = ref('')
const errorMessage = ref('')
const isLoading = ref(false)
const emailSent = ref(false)

// Handle form submission
async function handleSubmit() {
  // Reset error states
  emailError.value = ''
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
  
  try {
    isLoading.value = true
    await authApi.requestPasswordReset(email.value)
    emailSent.value = true
  } catch (error) {
    errorMessage.value = 
      error.response?.data?.detail || 
      'Unable to send reset link. Please try again later.'
  } finally {
    isLoading.value = false
  }
}

// Reset the form
function resetForm() {
  email.value = ''
  emailError.value = ''
  errorMessage.value = ''
  emailSent.value = false
}
</script>

<style scoped>
.forgot-password-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f0f2f5;
  padding: 1rem;
}

.forgot-password-container {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  width: 100%;
  max-width: 450px;
}

h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #333;
}

.instructions {
  margin-bottom: 1.5rem;
  color: #666;
  text-align: center;
}

.submit-btn {
  width: 100%;
  margin-top: 1.5rem;
}

.error-message {
  color: #dc3545;
  text-align: center;
  margin-top: 1rem;
}

.success-container {
  text-align: center;
}

.success-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 60px;
  height: 60px;
  background-color: #28a745;
  color: white;
  font-size: 2rem;
  border-radius: 50%;
  margin-bottom: 1rem;
}

.note {
  font-size: 0.9rem;
  color: #666;
  margin: 1rem 0;
}

.back-btn {
  margin-top: 1rem;
}

.login-link {
  display: block;
  margin-top: 1rem;
  color: #007bff;
  text-align: center;
}

.login-link:hover {
  text-decoration: underline;
}
</style>
