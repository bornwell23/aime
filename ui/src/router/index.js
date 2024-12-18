import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Dashboard from '../views/Dashboard.vue'
import History from '../views/History.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home,
    meta: { requiresAuth: true }
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/history',
    name: 'history',
    component: History,
    meta: { requiresAuth: true }
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
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// Navigation guard to check authentication
router.beforeEach((to, from, next) => {
  const authToken = localStorage.getItem('authToken');
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);

  if (requiresAuth && !authToken) {
    // Redirect to login with firstTimeUser flag if no accounts exist
    next({ 
      path: '/login', 
      query: { firstTimeUser: 'true' } 
    });
  } else if ((to.name === 'login' || to.name === 'register') && authToken) {
    // Redirect to dashboard if already authenticated and trying to access login/register
    next('/dashboard');
  } else {
    next();
  }
});

export default router
