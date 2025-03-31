<template>
    <form @submit.prevent="handleRegister" class="register-form">
      <div class="form-group">
        <base-input
          id="username"
          label="Username"
          v-model="username"
          :error="usernameError"
          :disabled="isLoading"
          placeholder="Choose a username"
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
          placeholder="Enter your email"
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
          placeholder="Repeat your password"
          required
        />
      </div>
  
      <base-button
        type="submit"
        :disabled="isLoading"
        variant="primary"
        class="submit-btn"
      >
        {{ isLoading ? 'Registering...' : 'Register' }}
      </base-button>
  
      <p v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </p>
  
      <p class="login-link">
        Already have an account? 
        <router-link to="/login">Login here</router-link>
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
  const username = ref('')
  const email = ref('')
  const password = ref('')
  const confirmPassword = ref('')
  const errorMessage = ref('')
  const isLoading = ref(false)
  
  // Error state for specific fields
  const usernameError = ref('')
  const emailError = ref('')
  const passwordError = ref('')
  const confirmPasswordError = ref('')
  
  // Auth store and router
  const authStore = useAuthStore()
  const router = useRouter()
  
  // Registration handler
  async function handleRegister() {
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
  
    // Validate password match
    const passwordMatchValidation = validate(
      password.value,
      validators.passwordMatch(confirmPassword.value)
    )
    if (passwordMatchValidation !== true) {
      confirmPasswordError.value = passwordMatchValidation
      return
    }
  
    try {
      isLoading.value = true
      await authStore.register({
        username: username.value,
        email: email.value,
        password: password.value,
        password2: confirmPassword.value
      })
    } catch (error) {
      // Handle registration errors
      errorMessage.value = error.response?.data?.detail 
        || 'Registration failed. Please try again.'
    } finally {
      isLoading.value = false
    }
  }
  </script>
  
  <style scoped>
  .register-form {
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
  
  .login-link {
    text-align: center;
    margin-top: 1.5rem;
  }
  
  .login-link a {
    color: #007bff;
    text-decoration: none;
    font-weight: 500;
  }
  
  .login-link a:hover {
    text-decoration: underline;
  }
  </style>