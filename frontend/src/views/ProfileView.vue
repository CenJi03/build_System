<template>
    <div class="profile-page">
      <div class="profile-container">
        <h1>User Profile</h1>
        
        <form @submit.prevent="updateProfile" class="profile-form">
          <div class="form-group">
            <base-input
              id="username"
              label="Username"
              v-model="username"
              :error="usernameError"
              :disabled="isLoading"
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
            />
          </div>
  
          <div class="password-section">
            <h2>Change Password</h2>
            <div class="form-group">
              <base-input
                id="current-password"
                label="Current Password"
                type="password"
                v-model="currentPassword"
                :error="currentPasswordError"
                :disabled="isLoading"
              />
            </div>
  
            <div class="form-group">
              <base-input
                id="new-password"
                label="New Password"
                type="password"
                v-model="newPassword"
                :error="newPasswordError"
                :disabled="isLoading"
              />
            </div>
  
            <div class="form-group">
              <base-input
                id="confirm-new-password"
                label="Confirm New Password"
                type="password"
                v-model="confirmNewPassword"
                :error="confirmNewPasswordError"
                :disabled="isLoading"
              />
            </div>
          </div>
  
          <div class="profile-actions">
            <base-button 
              type="submit" 
              :disabled="isLoading"
              variant="primary"
            >
              {{ isLoading ? 'Updating...' : 'Update Profile' }}
            </base-button>
            
            <base-button 
              type="button" 
              @click="cancelEdit"
              variant="secondary"
              :disabled="isLoading"
            >
              Cancel
            </base-button>
          </div>
  
          <div v-if="successMessage" class="success-message">
            {{ successMessage }}
          </div>
  
          <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </div>
        </form>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useAuthStore } from '@/stores/auth'
  import { useRouter } from 'vue-router'
  import BaseInput from '@/components/UI/BaseInput.vue'
  import BaseButton from '@/components/UI/BaseButton.vue'
  import { validators, validate } from '@/utils/validators'
  
  // Auth store and router
  const authStore = useAuthStore()
  const router = useRouter()
  
  // Form state
  const username = ref('')
  const email = ref('')
  const currentPassword = ref('')
  const newPassword = ref('')
  const confirmNewPassword = ref('')
  
  // Error and loading states
  const usernameError = ref('')
  const emailError = ref('')
  const currentPasswordError = ref('')
  const newPasswordError = ref('')
  const confirmNewPasswordError = ref('')
  const isLoading = ref(false)
  const successMessage = ref('')
  const errorMessage = ref('')
  
  // Fetch user profile on mount
  onMounted(async () => {
    try {
      const user = await authStore.fetchUserProfile()
      username.value = user.username
      email.value = user.email
    } catch (error) {
      errorMessage.value = 'Failed to load profile'
    }
  })
  
  // Validation method
  function validateForm() {
    // Reset previous errors
    usernameError.value = ''
    emailError.value = ''
    currentPasswordError.value = ''
    newPasswordError.value = ''
    confirmNewPasswordError.value = ''
  
    // Validate username
    const usernameValidation = validate(
      username.value,
      validators.required,
      validators.minLength(3),
      validators.maxLength(20)
    )
    if (usernameValidation !== true) {
      usernameError.value = usernameValidation
      return false
    }
  
    // Validate email
    const emailValidation = validate(
      email.value,
      validators.required,
      validators.email
    )
    if (emailValidation !== true) {
      emailError.value = emailValidation
      return false
    }
  
    // If password change is attempted
    if (currentPassword.value || newPassword.value || confirmNewPassword.value) {
      // Validate current password
      if (!currentPassword.value) {
        currentPasswordError.value = 'Current password is required'
        return false
      }
  
      // Validate new password
      const newPasswordValidation = validate(
        newPassword.value,
        validators.required,
        validators.passwordStrength
      )
      if (newPasswordValidation !== true) {
        newPasswordError.value = newPasswordValidation
        return false
      }
  
      // Validate password match
      const passwordMatchValidation = validate(
        newPassword.value,
        validators.passwordMatch(confirmNewPassword.value)
      )
      if (passwordMatchValidation !== true) {
        confirmNewPasswordError.value = passwordMatchValidation
        return false
      }
    }
  
    return true
  }
  
  // Update profile method
  async function updateProfile() {
    // Reset messages
    successMessage.value = ''
    errorMessage.value = ''
  
    // Validate form
    if (!validateForm()) {
      return
    }
  
    try {
      isLoading.value = true
  
      // Prepare update data
      const updateData = {
        username: username.value,
        email: email.value
      }
  
      // Add password fields if provided
      if (currentPassword.value) {
        updateData.current_password = currentPassword.value
        updateData.new_password = newPassword.value
      }
  
      // Update profile
      await authStore.updateUserProfile(updateData)
  
      // Clear password fields
      currentPassword.value = ''
      newPassword.value = ''
      confirmNewPassword.value = ''
  
      // Show success message
      successMessage.value = 'Profile updated successfully'
    } catch (error) {
      // Handle error
      errorMessage.value = error.response?.data?.detail 
        || 'Failed to update profile'
    } finally {
      isLoading.value = false
    }
  }
  
  // Cancel editing
  function cancelEdit() {
    router.push('/dashboard')
  }
  </script>
  
  <style scoped>
  .profile-page {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background-color: #f0f2f5;
    padding: 2rem;
  }
  
  .profile-container {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    padding: 2rem;
    width: 100%;
    max-width: 500px;
  }
  
  h1 {
    text-align: center;
    margin-bottom: 1.5rem;
    color: #333;
  }
  
  .password-section {
    margin-top: 1.5rem;
    padding-top: 1.5rem;
    border-top: 1px solid #e0e4e8;
  }
  
  .password-section h2 {
    font-size: 1.2rem;
    margin-bottom: 1rem;
    color: #666;
  }
  
  .form-group {
    margin-bottom: 1rem;
  }
  
  .profile-actions {
    display: flex;
    justify-content: space-between;
    margin-top: 1.5rem;
  }
  
  .success-message {
    color: #28a745;
    text-align: center;
    margin-top: 1rem;
  }
  
  .error-message {
    color: #dc3545;
    text-align: center;
    margin-top: 1rem;
  }
  </style>
