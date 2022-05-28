import { createRouter, createWebHistory } from 'vue-router'
import store from "@/store";
import Home from '../views/Home.vue'
import Login from "@/views/Login";
import Profile from "@/views/Profile";
import Schedule from "@/views/Schedule";

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/schedule/:company',
    name: 'Schedule',
    component: Schedule,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: {
      requiresAuth: false
    }
  },
  {
    path: '/about',
    name: 'About',
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!store.getters.isLoggedIn) {
      next({ name: 'Login' })
    } else {
      next()
    }
  }
  else if(store.getters.isLoggedIn){
    next({ name: 'Home' })
  } else {
    next()
  }
})

export default router
