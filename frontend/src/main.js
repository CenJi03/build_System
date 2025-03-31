import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

// Import global styles
import './assets/main.css'

// Create Vue application
const app = createApp(App)

// Create Pinia store
const pinia = createPinia()

// Configure plugins
app.use(pinia)   // State management
app.use(router)  // Vue Router

// Mount the application
app.mount('#app')