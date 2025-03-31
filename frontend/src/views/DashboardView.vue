<template>
  <div class="dashboard">
    <header class="dashboard-header">
      <h1>Welcome to Your Dashboard</h1>
      <div class="user-info">
        <p>Hello, {{ user?.username || 'User' }}!</p>
        <button @click="logout" class="logout-btn">Logout</button>
      </div>
    </header>

    <main class="dashboard-content">
      <section class="quick-stats">
        <div class="stat-card">
          <h3>Account Status</h3>
          <p>
            {{ user?.is_verified ? 'Verified' : 'Not Verified' }}
          </p>
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
    </main>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'

const authStore = useAuthStore()
const { user } = storeToRefs(authStore)

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
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  background-color: #f4f6f9;
  min-height: 100vh;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e0e4e8;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logout-btn {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

.quick-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 2rem;
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
}

.action-buttons {
  display: flex;
  gap: 1rem;
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
  margin-left: 1rem;
}
</style>