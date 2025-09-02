<template>
  <header class="app-header">
    <div class="container">
      <nav class="main-nav">
        <div class="logo">
          <router-link to="/">FeedMusic首页</router-link>
        </div>
        <ul class="nav-links">
          <li>
            <router-link to="/news" class="nav-link">新闻动态</router-link>
          </li>
        </ul>
        <div class="auth-buttons">
          <button 
            class="logout-btn" 
            @click="handleLogout"
            v-if="isAuthenticated"
          >
            退出登录
          </button>
          <button 
            class="login-btn"
            @click="openLoginModal"
            v-else
          >
            登录
          </button>
        </div>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted, inject } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isAuthenticated = ref(false)

// 注入全局的打开登录弹窗方法
const openLoginModal = inject('openLoginModal')

// 检查登录状态
const checkAuthStatus = () => {
  const token = localStorage.getItem('token')
  isAuthenticated.value = !!token
}

// 处理退出登录
const handleLogout = () => {
  if (confirm('确定要退出登录吗？')) {
    // 清除本地存储
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    isAuthenticated.value = false
    // 跳转到首页
    router.push('/')
  }
}

// 页面挂载时检查登录状态
onMounted(() => {
  checkAuthStatus()
})
</script>

<style scoped>
.app-header {
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 1rem 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.main-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo a {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
  text-decoration: none;
}

.nav-links {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
}

.nav-links li {
  margin-left: 2rem;
}

.nav-link {
  color: #333;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.nav-link:hover,
.nav-link.router-link-exact-active {
  color: #007bff;
}

.auth-buttons {
  display: flex;
  gap: 1rem;
}

.login-btn,
.logout-btn {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
}

.login-btn {
  background-color: #007bff;
  color: white;
  border: none;
}

.login-btn:hover {
  background-color: #0056b3;
}

.logout-btn {
  background-color: #dc3545;
  color: white;
  border: none;
}

.logout-btn:hover {
  background-color: #bb2d3b;
}
</style>
