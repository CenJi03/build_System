<template>
  <div class="profile-page">
    <div class="profile-container">
      <h1>User Profile</h1>
      
      <form @submit.prevent="updateProfile" class="profile-form">
        <div class="form-group">
          <label for="username">Username</label>
          <input 
            type="text" 
            id="username" 
            v-model="username" 
            required
            :disabled="isLoading"
          />
          <span v-if="usernameError" class="error">{{ usernameError }}</span>
        </div>

        <div class="form-group">
          <label for="email">Email</label>
          <input 
            type="email" 
            id="email" 
            v-model="email" 
            required
            :disabled="isLoading"
          />
          <span v-if="emailError" class="error">{{ emailError }}</span>
        </div>

        <div class="password-section">
          <h2>Change Password</h2>
          <div class="form-group">
            <label for="current-password">Current Password</label>
            <div class="password-input-container">
              <input 
                :type="showCurrentPassword ? 'text' : 'password'" 
                id="current-password" 
                v-model="currentPassword"
                :disabled="isLoading"
              />
              <button 
                type="button" 
                @click="showCurrentPassword = !showCurrentPassword" 
                class="toggle-password"
              >
                {{ showCurrentPassword ? '🔒' : '👁️' }}
              </button>
            </div>
            <span v-if="currentPasswordError" class="error">
              {{ currentPasswordError }}
            </span>
          </div>

          <div class="form-group">
            <label for="new-password">New Password</label>
            <div class="password-input-container">
              <input 
                :type="showNewPassword ? 'text' : 'password'" 
                id="new-password" 
                v-model="newPassword"
                :disabled="isLoading"
              />
              <button 
                type="button" 
                @click="showNewPassword = !showNewPassword" 
                class="toggle-password"
              >
                {{ showNewPassword ? '🔒' : '👁️' }}
              </button>
            </div>
            <span v-if="newPasswordError" class="error">
              {{ newPasswordError }}
            </span>
            <div v-if="newPassword" class="password-strength-indicator">
              <div class="strength-meter">
                <div 
                  class="strength-meter-fill" 
                  :style="{ width: passwordStrength.score + '%', backgroundColor: passwordStrength.color }"
                ></div>
              </div>
              <span :style="{ color: passwordStrength.color }">{{ passwordStrength.label }}</span>
            </div>
          </div>

          <div class="form-group">
            <label for="confirm-new-password">Confirm New Password</label>
            <div class="password-input-container">
              <input 
                :type="showConfirmPassword ? 'text' : 'password'" 
                id="confirm-new-password" 
                v-model="confirmNewPassword"
                :disabled="isLoading"
              />
              <button 
                type="button" 
                @click="showConfirmPassword = !showConfirmPassword" 
                class="toggle-password"
              >
                {{ showConfirmPassword ? '🔒' : '👁️' }}
              </button>
            </div>
            <span v-if="confirmNewPasswordError" class="error">
              {{ confirmNewPasswordError }}
            </span>
          </div>
        </div>

        <div class="profile-actions">
          <button 
            type="submit" 
            :disabled="isLoading"
            class="update-btn"
          >
            {{ isLoading ? 'Updating...' : 'Update Profile' }}
          </button>
          
          <button 
            type="button" 
            @click="cancelEdit"
            class="cancel-btn"
            :disabled="isLoading"
          >
            Cancel
          </button>
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
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
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

// Password visibility state
const showCurrentPassword = ref(false)
const showNewPassword = ref(false)
const showConfirmPassword = ref(false)

// Password strength calculator
const passwordStrength = computed(() => {
  if (!newPassword.value) return { score: 0, color: '#ccc', label: '' }
  
  let score = 0
  let color = ''
  let label = ''
  
  // Length check
  if (newPassword.value.length >= 8) score += 20
  if (newPassword.value.length >= 12) score += 10
  
  // Complexity checks
  if (/[A-Z]/.test(newPassword.value)) score += 20
  if (/[a-z]/.test(newPassword.value)) score += 15
  if (/[0-9]/.test(newPassword.value)) score += 15
  if (/[^A-Za-z0-9]/.test(newPassword.value)) score += 20
  
  // Determine color and label
  if (score < 30) {
    color = '#ff4d4d'
    label = 'Weak'
  } else if (score < 60) {
    color = '#ffa64d'
    label = 'Moderate'
  } else if (score < 80) {
    color = '#4db8ff'
    label = 'Strong'
  } else {
    color = '#66cc66'
    label = 'Very Strong'
  }
  
  return { score, color, label }
})

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
      validators.passwordStrength,
      (val) => (passwordStrength.value.score >= 60) || 'Password is not strong enough'
    )
    if (newPasswordValidation !== true) {
      newPasswordError.value = newPasswordValidation
      return false
    }

    // Validate password match
    const passwordMatchValidation = validate(
      newPassword.value,
      validators.required,
      (val) => val ===
      confirmNewPassword.value
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

input:disabled {
  background-color: #f4f4f4;
  cursor: not-allowed;
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

.profile-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 1.5rem;
}

.update-btn, .cancel-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

.update-btn {
  background-color: #28a745;
  color: white;
}

.cancel-btn {
  background-color: #6c757d;
  color: white;
}

.update-btn:disabled, .cancel-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.error {
  color: #dc3545;
  font-size: 0.8rem;
  margin-top: 0.5rem;
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

.password-input-container {
  position: relative;
  display: flex;
  align-items: center;
}

.toggle-password {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  padding: 0;
  color: #666;
}

.password-strength-indicator {
  margin-top: 0.5rem;
}

.strength-meter {
  height: 6px;
  background-color: #e0e0e0;
  border-radius: 3px;
  overflow: hidden;
}

.strength-meter-fill {
  height: 100%;
  transition: width 0.3s ease-in-out, background-color 0.3s ease-in-out;
}
</style>