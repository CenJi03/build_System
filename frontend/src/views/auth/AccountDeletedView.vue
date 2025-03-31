<template>
  <div class="account-deleted-page">
    <div class="account-deleted-container">
      <div class="icon-container">
        <span class="check-icon">✓</span>
      </div>
      
      <h1>Account Deleted</h1>
      
      <p>
        Your account has been successfully deleted. All your personal data has been removed from our systems.
      </p>
      
      <div class="action-buttons">
        <base-button 
          @click="goToHome" 
          variant="primary"
        >
          Return to Home
        </base-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import BaseButton from '@/components/UI/BaseButton.vue'

const router = useRouter()

function goToHome() {
  router.push('/')
}
</script>

<style scoped>
.account-deleted-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f0f2f5;
  padding: 2rem;
}

.account-deleted-container {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 3rem 2rem;
  text-align: center;
  max-width: 500px;
  width: 100%;
}

.icon-container {
  margin-bottom: 1.5rem;
}

.check-icon {
  display: inline-flex;
  justify-content: center;
  align-items: center;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  font-size: 2.5rem;
  background-color: #28a745;
  color: white;
}

h1 {
  margin-bottom: 1.5rem;
  color: #333;
}

p {
  margin-bottom: 2rem;
  color: #666;
  font-size: 1.1rem;
  line-height: 1.6;
}

.action-buttons {
  margin-top: 1rem;
}
</style>
