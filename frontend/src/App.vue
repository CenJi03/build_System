<template>
  <div id="app">
    <div v-if="notification.show" class="notification" :class="notification.type">
      {{ notification.message }}
    </div>
    
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useAuthStore } from '@/stores/auth'

// Create a simple notification system
const notification = reactive({
  show: false,
  message: '',
  type: 'success',
  timeout: null
})

// Show notification
function showNotification(message, type = 'success', duration = 3000) {
  if (notification.timeout) {
    clearTimeout(notification.timeout)
  }
  
  notification.show = true
  notification.message = message
  notification.type = type
  
  notification.timeout = setTimeout(() => {
    notification.show = false
  }, duration)
}

// Listen for successful login
const authStore = useAuthStore()
authStore.$subscribe((mutation, state) => {
  if (state.isAuthenticated && !mutation.oldState.isAuthenticated) {
    showNotification(`Welcome ${state.user?.username || 'back'}! You've successfully logged in.`)
  }
})
</script>

<style>
.notification {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 15px 20px;
  border-radius: 4px;
  color: white;
  z-index: 1000;
  animation: slide-in 0.3s ease-out;
}

.notification.success {
  background-color: #28a745;
}

.notification.error {
  background-color: #dc3545;
}

.notification.info {
  background-color: #17a2b8;
}

@keyframes slide-in {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}
</style>