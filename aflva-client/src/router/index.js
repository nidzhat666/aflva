import { createRouter, createWebHistory } from 'vue-router'
import Auth from '../views/Auth.vue'
import Book from '../views/Book.vue'
import Flight from '../views/Flight.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Auth
  },
  {
    path: '/books',
    name: 'Book',
    component: Book
  },
  {
    path: '/flight',
    name: 'Flight',
    component: Flight
  },
  {
    path: '/',
    name: 'About',
    component: () => import( '../views/About.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
