<template>
  <div class="setup-2fa-page">
    <base-card title="Set Up Two-Factor Authentication" class="setup-2fa-card">
      <template v-if="isLoading">
        <div class="loading-state">
          <p>Loading...</p>
        </div>
      </template>
      
      <template v-else-if="step === 'setup'">
        <div class="setup-container">
          <p class="info-text">
            Two-factor authentication adds an extra layer of security to your account by requiring both your password and a verification code from your mobile device.
          </p>
          
          <div v-if="qrCodeUrl" class="qr-code-container">
            <h3>Scan QR Code</h3>
            <p>Scan this QR code with your authenticator app:</p>
            <img :src="qrCodeUrl" alt="QR Code for two-factor authentication" class="qr-code" />
            
            <div class="manual-entry">
              <h4>Or enter secret key manually:</h4>
              <div class="secret-key">{{ secretKey }}</div>
            </div>
          </div>
          
          <form @submit.prevent="verifyCode" class="verification-form">
            <div class="form-group">
              <base-input
                id="verificationCode"
                label="Verification Code"
                v-model="verificationCode"
                :error="codeError"
                placeholder="Enter 6-digit code"
                required
              />
            </div>
            
            <div class="action-buttons">
              <base-button 
                type="submit" 
                variant="primary" 
                :disabled="!qrCodeUrl || verifyingCode"
              >
                {{ verifyingCode ? 'Verifying...' : 'Verify & Activate' }}
              </base-button>
              
              <base-button 
                type="button" 
                variant="secondary"
                @click="cancelSetup"
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
      
      <template v-else-if="step === 'success'">
        <div class="success-state">
          <div class="icon-container">
            <span class="success-icon">✓</span>
          </div>
          <h3>Two-Factor Authentication Enabled</h3>
          <p>
            Your account is now secured with two-factor authentication. You will need your authenticator app to sign in from now on.
          </p>
          <base-button 
            variant="primary" 
            @click="goToDashboard" 
            full-width
          >
            Return to Dashboard
          </base-button>
        </div>
      </template>
    </base-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import BaseCard from '@/components/UI/BaseCard.vue'
import BaseButton from '@/components/UI/BaseButton.vue'
import BaseInput from '@/components/UI/BaseInput.vue'

const router = useRouter()
const authStore = useAuthStore()

const isLoading = ref(true)
const step = ref('setup')
const qrCodeUrl = ref('')
const secretKey = ref('')
const verificationCode = ref('')
const codeError = ref('')
const errorMessage = ref('')
const verifyingCode = ref(false)

onMounted(async () => {
  try {
    const response = await authStore.setup2FA()
    qrCodeUrl.value = response.uri
    secretKey.value = response.secret
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Failed to set up two-factor authentication.'
  } finally {
    isLoading.value = false
  }
})

async function verifyCode() {
  if (!verificationCode.value) {
    codeError.value = 'Verification code is required'
    return
  }
  
  if (!/^\d{6}$/.test(verificationCode.value)) {
    codeError.value = 'Code must be 6 digits'
    return
  }
  
  codeError.value = ''
  errorMessage.value = ''
  verifyingCode.value = true
  
  try {
    await authStore.verify2FA(verificationCode.value)
    step.value = 'success'
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Invalid verification code. Please try again.'
  } finally {
    verifyingCode.value = false
  }
}

function cancelSetup() {
  router.push('/dashboard')
}

function goToDashboard() {
  router.push('/dashboard')
}
</script>

<style scoped>
.setup-2fa-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f0f2f5;
  padding: 2rem;
}

.setup-2fa-card {
  width: 100%;
  max-width: 500px;
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

.info-text {
  margin-bottom: 1.5rem;
  color: #666;
}

.qr-code-container {
  text-align: center;
  margin-bottom: 2rem;
}

.qr-code {
  max-width: 200px;
  height: auto;
  margin: 1rem auto;
  padding: 0.5rem;
  background-color: white;
  border: 1px solid #ddd;
}

.manual-entry {
  margin-top: 1rem;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.secret-key {
  font-family: monospace;
  font-size: 1.2rem;
  padding: 0.5rem;
  margin-top: 0.5rem;
  background-color: #e9ecef;
  border-radius: 4px;
  word-break: break-all;
}

.verification-form {
  margin-top: 1.5rem;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.error-message {
  color: #dc3545;
  margin-top: 1rem;
  text-align: center;
}
</style>
