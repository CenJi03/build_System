<template>
  <div class="not-found-container">
    <div class="not-found-content">
      <h1>404</h1>
      <h2>Page Not Found</h2>
      <p>Sorry, the page you are looking for doesn't exist or has been moved.</p>
      <div class="actions">
        <router-link to="/" class="btn btn-home">
          Go to Home
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
// No additional logic needed
</script>

<style scoped>
.not-found-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f0f2f5;
  padding: 2rem;
}

.not-found-content {
  text-align: center;
  background-color: white;
  border-radius: 8px;
  padding: 3rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 500px;
  width: 100%;
}

h1 {
  font-size: 6rem;
  color: #dc3545;
  margin-bottom: 1rem;
}

h2 {
  font-size: 2rem;
  color: #333;
  margin-bottom: 1rem;
}

p {
  color: #666;
  margin-bottom: 2rem;
}

.actions {
  display: flex;
  justify-content: center;
}

.btn-home {
  display: inline-block;
  background-color: #007bff;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  text-decoration: none;
  transition: background-color 0.3s ease;
}

.btn-home:hover {
  background-color: #0056b3;
}
</style>