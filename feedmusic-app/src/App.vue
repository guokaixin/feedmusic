<template>
  <div id="app">
    <Header />
    <main class="main-content">
      <RouterView />
    </main>
    <!-- 登录弹窗组件 -->
    <LoginModal ref="loginModalRef" @login-success="handleLoginSuccess" />
    <Footer />
  </div>
</template>

<script setup>
import { ref, provide } from 'vue'
import Header from './components/Header.vue'
import Footer from './components/Footer.vue'
import LoginModal from './components/LoginModal.vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const loginModalRef = ref(null)

// 提供全局打开登录弹窗的方法
provide('openLoginModal', () => {
  if (loginModalRef.value) {
    loginModalRef.value.openModal()
  }
})

// 登录成功后的处理
const handleLoginSuccess = (userData) => {
  localStorage.setItem('token', userData.token)
  localStorage.setItem('user', JSON.stringify(userData.user))
  // 重新加载当前页面以更新状态
  router.go(0)
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  color: #333;
  line-height: 1.6;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  padding: 20px 0;
}
</style>
