import { createRouter, createWebHistory } from 'vue-router'
import Introduction from '../views/Introduction.vue'
import News from '../views/News.vue'
import AdminNewsForm from '../views/AdminNewsForm.vue'

const routes = [
  {
    path: '/',
    name: 'Introduction',
    component: Introduction
  },
  {
    path: '/news',
    name: 'News',
    component: News,
    meta: { requiresAuth: true } // 需要登录才能访问
  },
  {
    path: '/admin/news/create',
    name: 'CreateNews',
    component: AdminNewsForm,
    meta: { requiresAuth: true }
  },
  {
    path: '/admin/news/edit/:id',
    name: 'EditNews',
    component: AdminNewsForm,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫 - 验证登录状态
router.beforeEach((to, from, next) => {
  // 检查路由是否需要登录
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // 检查本地存储中是否有token
    const token = localStorage.getItem('token')
    if (!token) {
      // 未登录，重定向到首页
      next({ name: 'Introduction' })
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router
