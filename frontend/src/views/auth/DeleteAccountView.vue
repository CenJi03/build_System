<template>
  <div class="delete-account-page">
    <base-card title="Delete Account" class="delete-account-card">
      <template v-if="isLoading">
        <div class="loading-state">
          <p>Processing your request...</p>
        </div>
      </template>
      
      <template v-else>
        <div class="warning-container">
          <div class="icon-container">
            <span class="warning-icon">!</span>
          </div>
          <h3>Delete Your Account</h3>
          <p>
            This action is <strong>permanent</strong> and cannot be undone. All your data will be permanently deleted.
          </p>
          
          <form @submit.prevent="confirmDeletion" class="confirmation-form">
            <div class="form-group">
              <base-input
                id="password"
                label="Enter your password to confirm"
                type="password"
                v-model="password"
                :error="passwordError"
                placeholder="Password"
                required
              />
            </div>
            
            <div class="checkbox-group">
              <input 
                type="checkbox" 
                id="confirmCheck" 
                v-model="confirmed" 
                required
              />
              <label for="confirmCheck">
                I understand that this action is irreversible
              </label>
            </div>
            
            <div class="action-buttons">
              <base-button 
                type="submit" 
                variant="danger" 
                :disabled="!confirmed || deleting"
              >
                {{ deleting ? 'Deleting Account...' : 'Delete My Account' }}
              </base-button>
              
              <base-button 
                type="button" 
                variant="secondary"
                @click="cancelDeletion"
              >
                Cancel
              </base-button>
            </div>
          </form>
          
          <p v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </p>
        </div>
      </template>
    </base-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import BaseCard from '@/components/UI/BaseCard.vue'
import BaseButton from '@/components/UI/BaseButton.vue'
import BaseInput from '@/components/UI/BaseInput.vue'

const router = useRouter()
const authStore = useAuthStore()

const isLoading = ref(false)
const password = ref('')
const passwordError = ref('')
const confirmed = ref(false)
const errorMessage = ref('')
const deleting = ref(false)

async function confirmDeletion() {
  if (!password.value) {
    passwordError.value = 'Password is required'
    return
  }
  
  if (!confirmed.value) {
    errorMessage.value = 'Please confirm that you understand this action is irreversible'
    return
  }
  
  passwordError.value = ''
  errorMessage.value = ''
  deleting.value = true
  
  try {
    await authStore.deleteAccount(password.value)
    // The store's deleteAccount method will redirect to the account-deleted page
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Failed to delete account. Please check your password and try again.'
    deleting.value = false
  }
}

function cancelDeletion() {
  router.push('/dashboard')
}
</script>

<style scoped>
.delete-account-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f0f2f5;
  padding: 2rem;
}

.delete-account-card {
  width: 100%;
  max-width: 500px;
}

.loading-state {
  text-align: center;
  padding: 1rem;
}

.warning-container {
  text-align: center;
}

.icon-container {
  margin-bottom: 1rem;
}

.warning-icon {
  display: inline-flex;
  justify-content: center;
  align-items: center;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  font-size: 2rem;
  background-color: #ffc107;
  color: #212529;
  margin-bottom: 1rem;
  font-weight: bold;
}

.confirmation-form {
  margin-top: 2rem;
  text-align: left;
}

.checkbox-group {
  margin: 1.5rem 0;
  display: flex;
  align-items: center;
}

.checkbox-group input {
  margin-right: 0.5rem;
}

.action-buttons {
  display: flex;
  gap: 1rem;
}

.error-message {
  color: #dc3545;
  margin-top: 1rem;
}
</style>
