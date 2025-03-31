<template>
  <div class="dashboard">
    <div class="welcome-banner">
      <h1>Welcome to Your Dashboard, {{ username }}!</h1>
      <p>You have successfully logged in.</p>
    </div>
    
    <div class="dashboard-content">
      <section class="quick-stats">
        <div class="stat-card">
          <h3>Account Status</h3>
          <p>{{ user?.is_verified ? 'Verified' : 'Not Verified' }}</p>
        </div>
        <div class="stat-card">
          <h3>Email</h3>
          <p>{{ user?.email || 'Not available' }}</p>
        </div>
      </section>

      <section class="actions">
        <h2>Quick Actions</h2>
        <div class="action-buttons">
          <router-link to="/profile" class="btn btn-profile">
            Edit Profile
          </router-link>
          <router-link v-if="user?.is_staff" to="/admin-signup" class="btn btn-admin">
            Create Admin Account
          </router-link>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'

const authStore = useAuthStore()
const { user } = storeToRefs(authStore)

// Compute a proper greeting name (username, first name, or generic)
const username = computed(() => {
  if (user.value?.first_name) return user.value.first_name
  if (user.value?.username) return user.value.username
  return 'User'
})

onMounted(async () => {
  // Fetch user profile when dashboard is loaded
  if (!user.value) {
    await authStore.fetchUserProfile()
  }
})

function logout() {
  authStore.logout()
}
</script>

<style scoped>
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.welcome-banner {
  background-color: #f0f7ff;
  border-left: 4px solid #007bff;
  padding: 1.5rem;
  margin-bottom: 2rem;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.welcome-banner h1 {
  margin-bottom: 0.5rem;
  color: #007bff;
}

.welcome-banner p {
  margin: 0;
  color: #555;
}

.dashboard-content {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
}

@media (min-width: 768px) {
  .dashboard-content {
    grid-template-columns: 1fr 1fr;
  }
}

.quick-stats {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

@media (min-width: 768px) {
  .quick-stats {
    grid-template-columns: 1fr 1fr;
  }
}

.stat-card {
  background-color: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.stat-card h3 {
  margin-bottom: 0.5rem;
  color: #666;
}

.actions {
  background-color: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  grid-column: 1 / -1;
}

.action-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 1rem;
}

.btn {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  text-decoration: none;
  border-radius: 4px;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

.btn-profile {
  background-color: #28a745;
  color: white;
}

.btn-admin {
  background-color: #6f42c1;
  color: white;
}
</style>