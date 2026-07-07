import { createRouter, createWebHistory } from 'vue-router'
import Login from './views/Login.vue'
import Signup from './views/Signup.vue'
import AdminDashboard from './views/AdminDashboard.vue'\nimport UserDashboard from './views/UserDashboard.vue'
import { getToken, getUserRole } from './api/auth'

const routes = [
    { path: '/', redirect: '/login' },
    { path: '/login', component: Login },
    { path: '/signup', component: Signup },
    { path: '/admin', component: AdminDashboard, meta: { requiresAuth: true, role: 'admin' } },
    { path: '/dashboard', component: UserDashboard, meta: { requiresAuth: true, role: 'user' } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = getToken()
  const role = getUserRole()
  
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if (to.path === '/login' && token) {
    next(role === 'admin' ? '/admin' : '/dashboard')
  } else {
    next()
  }
})

export default router
