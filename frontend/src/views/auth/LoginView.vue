<template>
    <div class="login-page">
      <div class="login-container">
        <h2>Login to Your Account</h2>
        <LoginForm />
      </div>
    </div>
  </template>
  
  <script setup>
  import LoginForm from '@/components/auth/LoginForm.vue'
  </script>
  
  <style scoped>
  .login-page {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background-color: #f0f2f5;
  }
  
  .login-container {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    padding: 2rem;
    width: 100%;
    max-width: 400px;
  }
  
  h2 {
    text-align: center;
    margin-bottom: 1.5rem;
    color: #333;
  }
  </style>
