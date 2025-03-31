import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)) // Ensure this maps to the correct directory
    }
  },
  server: {
    port: 5173,
    host: true, // Listen on all addresses
    strictPort: true, // Don't try another port if this one is taken
    watch: {
      usePolling: true // Necessary for working in Docker containers with mounted volumes
    },
    proxy: {
      // Add API proxy for development
      '/api': {
        target: process.env.VITE_API_URL || 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  },
  // Optimize build for production
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    emptyOutDir: true,
    sourcemap: process.env.NODE_ENV !== 'production'
  }
})