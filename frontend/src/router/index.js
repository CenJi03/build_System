import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/HomeView.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/auth/LoginView.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../views/DashboardView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/ProfileView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/verify-email',
    name: 'VerifyEmail',
    component: () => import('../views/auth/VerifyEmailView.vue'),
    props: route => ({ token: route.query.token })
  },
  {
    path: '/reset-password',
    name: 'ResetPassword',
    component: () => import('../views/auth/ResetPasswordView.vue'),
    props: route => ({ token: route.query.token })
  },
  {
    path: '/setup-2fa',
    name: 'Setup2FA',
    component: () => import('../views/auth/Setup2FAView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/delete-account',
    name: 'DeleteAccount',
    component: () => import('../views/auth/DeleteAccountView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/account-deleted',
    name: 'AccountDeleted',
    component: () => import('../views/auth/AccountDeletedView.vue')
  },
  {
    path: '/admin-signup',
    name: 'AdminSignup',
    component: () => import('../views/auth/AdminSignupView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFoundView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// Navigation guards
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // Check if route requires auth and user is not authenticated
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
    return
  }

  // Check if route requires admin permissions
  if (to.meta.requiresAdmin && (!authStore.user || !authStore.user.is_staff)) {
    next('/dashboard')
    return
  }

  // If trying to access login when already authenticated, redirect to dashboard
  if (to.path === '/login' && authStore.isAuthenticated) {
    next('/dashboard')
    return
  }

  next()
})

export default router