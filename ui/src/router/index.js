import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Dashboard from '../views/Dashboard.vue'
import History from '../views/History.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import AuthGuard from '../components/AuthGuard.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home,
    meta: { requiresAuth: true },
    beforeEnter: (to, from, next) => {
      const authToken = localStorage.getItem('authToken');
      const loginAttempts = localStorage.getItem('loginAttempts');
      
      if (!authToken) {
        next({ 
          path: '/login', 
          query: { firstTimeUser: loginAttempts ? 'false' : 'true' } 
        });
      } else {
        next();
      }
    }
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: Dashboard,
    meta: { requiresAuth: true },
    beforeEnter: (to, from, next) => {
      const authToken = localStorage.getItem('authToken');
      const loginAttempts = localStorage.getItem('loginAttempts');
      
      if (!authToken) {
        next({ 
          path: '/login', 
          query: { firstTimeUser: loginAttempts ? 'false' : 'true' } 
        });
      } else {
        next();
      }
    }
  },
  {
    path: '/history',
    name: 'history',
    component: History,
    meta: { requiresAuth: true },
    beforeEnter: (to, from, next) => {
      const authToken = localStorage.getItem('authToken');
      const loginAttempts = localStorage.getItem('loginAttempts');
      
      if (!authToken) {
        next({ 
          path: '/login', 
          query: { firstTimeUser: loginAttempts ? 'false' : 'true' } 
        });
      } else {
        next();
      }
    }
  },
  {
    path: '/login',
    name: 'login',
    component: Login,
    props: (route) => ({ 
      firstTimeUser: route.query.firstTimeUser === 'true' 
    }),
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'register',
    component: Register,
    meta: { requiresAuth: false }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard to check authentication
router.beforeEach((to, from, next) => {
  const authToken = localStorage.getItem('authToken');
  
  if (to.meta.requiresAuth && !authToken) {
    const loginAttempts = localStorage.getItem('loginAttempts');
    next({ 
      path: '/login', 
      query: { firstTimeUser: loginAttempts ? 'false' : 'true' } 
    });
  } else if ((to.name === 'login' || to.name === 'register') && authToken) {
    next('/dashboard');
  } else {
    next();
  }
})

export default router
