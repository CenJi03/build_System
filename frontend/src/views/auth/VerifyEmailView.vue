<template>
  <div class="verify-email-page">
    <base-card title="Email Verification" class="verify-email-card">
      <template v-if="isLoading">
        <div class="loading-state">
          <p>Verifying your email...</p>
        </div>
      </template>
      
      <template v-else-if="isSuccess">
        <div class="success-state">
          <div class="icon-container">
            <span class="success-icon">✓</span>
          </div>
          <h2>Email Verified!</h2>
          <p>Your email has been successfully verified.</p>
          <base-button 
            variant="primary" 
            @click="goToLogin" 
            full-width
          >
            Continue to Login
          </base-button>
        </div>
      </template>
      
      <template v-else>
        <div class="error-state">
          <div class="icon-container">
            <span class="error-icon">✕</span>
          </div>
          <h2>Verification Failed</h2>
          <p>{{ errorMessage || 'We could not verify your email. The verification link may have expired.' }}</p>
          <base-button 
            variant="primary" 
            @click="goToLogin" 
            full-width
          >
            Back to Login
          </base-button>
        </div>
      </template>
    </base-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import BaseCard from '@/components/UI/BaseCard.vue'
import BaseButton from '@/components/UI/BaseButton.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const isLoading = ref(true)
const isSuccess = ref(false)
const errorMessage = ref('')

onMounted(async () => {
  const token = route.query.token

  if (!token) {
    isLoading.value = false
    errorMessage.value = 'Verification token is missing.'
    return
  }

  try {
    await authStore.verifyEmail(token)
    isSuccess.value = true
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Email verification failed.'
  } finally {
    isLoading.value = false
  }
})

function goToLogin() {
  router.push('/login')
}
</script>

<style scoped>
.verify-email-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f0f2f5;
  padding: 2rem;
}

.verify-email-card {
  width: 100%;
  max-width: 400px;
}

.loading-state,
.success-state,
.error-state {
  text-align: center;
  padding: 1rem;
}

.icon-container {
  margin-bottom: 1rem;
}

.success-icon,
.error-icon {
  display: inline-flex;
  justify-content: center;
  align-items: center;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  font-size: 2rem;
  margin-bottom: 1rem;
}

.success-icon {
  background-color: #28a745;
  color: white;
}

.error-icon {
  background-color: #dc3545;
  color: white;
}

h2 {
  margin-bottom: 1rem;
}

p {
  margin-bottom: 1.5rem;
  color: #666;
}
</style>
