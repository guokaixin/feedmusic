<template>
  <nav class="navbar">
    <div class="navbar-container">
      <div class="logo" @click="goToHome">
        <span>FeedMusic</span>
      </div>
      
      <div class="nav-links">
        <a href="#" @click.prevent="goToHome">首页</a>
        <a href="#" @click.prevent="goToNews">新闻动态</a>
      </div>
      
      <div class="auth-buttons">
        <button 
          v-if="!isAuthenticated" 
          class="login-btn" 
          @click="openLoginModal"
        >
          登录
        </button>
        
        <div v-if="isAuthenticated" class="user-menu">
          <span class="username">{{ user.username }}</span>
          <button class="logout-btn" @click="handleLogout">退出登录</button>
        </div>
      </div>
    </div>
    
    <!-- 登录模态框 -->
    <LoginModal 
      ref="loginModalRef" 
      @login-success="handleLoginSuccess"
    />
  </nav>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'  // 新增nextTick
import { useRouter } from 'vue-router'
import LoginModal from './LoginModal.vue'
import { authAPI } from '../services/api'

const router = useRouter()
const loginModalRef = ref(null)

// 状态管理
const isAuthenticated = ref(false)
const user = ref({})

// 检查登录状态
const checkAuthStatus = () => {
  try {
    const token = localStorage.getItem('token')
    const userData = localStorage.getItem('user')
    
    if (token && userData) {
      isAuthenticated.value = true
      user.value = JSON.parse(userData)
    } else {
      isAuthenticated.value = false
      user.value = {}
    }
  } catch (error) {
    console.error('检查登录状态失败', error)
    logout()
  }
}

// 打开登录模态框 - 新增nextTick确保DOM更新
const openLoginModal = async () => {
  console.log('尝试打开登录模态框', loginModalRef.value);
  if (loginModalRef.value) {
    await nextTick()  // 等待DOM更新
    loginModalRef.value.openModal()
  } else {
    console.error('登录模态框组件未正确加载');
    alert('登录功能加载失败，请刷新页面重试');
  }
}

// 处理登录成功
const handleLoginSuccess = (userData) => {
  isAuthenticated.value = true
  user.value = userData
  router.push('/news')
}

// 退出登录
const handleLogout = async () => {
  try {
    await authAPI.logout()
  } catch (error) {
    console.error('退出登录API调用失败', error)
  } finally {
    logout()
  }
}

// 清除登录状态
const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  isAuthenticated.value = false
  user.value = {}
  router.push('/')
}

// 页面导航
const goToHome = () => {
  router.push('/')
}

const goToNews = () => {
  router.push('/news')
}

// 初始化检查登录状态
onMounted(() => {
  checkAuthStatus()
})
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 70px;
  background-color: #fff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  z-index: 900;
}

.navbar-container {
  max-width: 1200px;
  height: 100%;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 24px;
  font-weight: bold;
  cursor: pointer;
  color: #333;
}

.nav-links {
  display: flex;
  gap: 20px;
}

.nav-links a {
  text-decoration: none;
  color: #333;
  font-size: 16px;
  transition: color 0.3s;
}

.nav-links a:hover {
  color: #007bff;
}

.auth-buttons {
  display: flex;
  align-items: center;
  gap: 10px;
}

.login-btn, .logout-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.login-btn {
  background-color: #007bff;
  color: white;
}

.login-btn:hover {
  background-color: #0056b3;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 15px;
}

.username {
  font-size: 16px;
  color: #333;
}

.logout-btn {
  background-color: #dc3545;
  color: white;
}

.logout-btn:hover {
  background-color: #bb2d3b;
}
</style>