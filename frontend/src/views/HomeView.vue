<template>
  <div class="home-container">
    <h1>Welcome to Our Application</h1>
    <p>Get started by logging in or creating an account.</p>
    <div class="action-buttons">
      <router-link to="/login" class="btn btn-login">
        Log In
      </router-link>
      <router-link to="/register" class="btn btn-register">
        Register
      </router-link>
    </div>
  </div>
</template>

<script setup>
// No additional logic needed for home page
</script>

<style scoped>
.home-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  text-align: center;
  padding: 2rem;
  background-color: #f0f2f5;
}

h1 {
  color: #333;
  margin-bottom: 1rem;
  font-size: 2.5rem;
}

p {
  color: #666;
  margin-bottom: 2rem;
  font-size: 1.2rem;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.btn {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  text-decoration: none;
  border-radius: 4px;
  font-weight: bold;
  transition: background-color 0.3s ease;
  font-size: 1rem;
}

.btn-login {
  background-color: #007bff;
  color: white;
}

.btn-register {
  background-color: #28a745;
  color: white;
}

.btn:hover {
  opacity: 0.9;
}
</style>
