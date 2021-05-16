import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../components/Homepage.vue')
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../components/Auth/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../components/Auth/Register.vue')
  },
  {
    path: '/logout',
    name: 'Logout',
    component: () => import('../components/Auth/Logout.vue')
  },
  {
    path: '/leaderboard',
    name: 'Leaderboard',
    component: () => import('../components/LeaderBoard/leaderboard.vue')
  },
  {
    path: '/matches',
    name: 'Matches',
    component: () => import('../components/Match/matches.vue')
  },
  {
    path: '/predict',
    name: 'Predict',
    component: () => import('../components/Prediction/predict.vue')
  },

]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
