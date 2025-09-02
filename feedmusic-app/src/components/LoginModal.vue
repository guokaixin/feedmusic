<template>
  <div class="modal-backdrop" v-if="isOpen" @click="closeModal(false)">
    <div class="modal-container" @click.stop>
      <div class="modal-header">
        <h2>登录</h2>
        <button class="close-btn" @click="closeModal(false)">×</button>
      </div>
      <div class="modal-body">
        <form @submit.prevent="handleLogin">
          <div class="form-group">
            <label for="username">用户名</label>
            <input
              type="text"
              id="username"
              v-model="credentials.username"
              required
              placeholder="请输入用户名"
            >
          </div>
          <div class="form-group">
            <label for="password">密码</label>
            <input
              type="password"
              id="password"
              v-model="credentials.password"
              required
              placeholder="请输入密码"
            >
          </div>
          <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </div>
          <button type="submit" class="login-btn" :disabled="isLoading">
            <span v-if="!isLoading">登录</span>
            <span v-if="isLoading">登录中...</span>
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineEmits, defineExpose } from 'vue'
import { authAPI } from '../services/api'

const emit = defineEmits(['login-success'])
const isOpen = ref(false)
const isLoading = ref(false)
const errorMessage = ref('')
const credentials = ref({
  username: '',
  password: ''
})

// 打开模态框
const openModal = () => {
  isOpen.value = true
  errorMessage.value = ''
  credentials.value = {
    username: '',
    password: ''
  }
}

// 关闭模态框
const closeModal = (isSuccess = false) => {
  isOpen.value = false
}

// 处理登录
const handleLogin = async () => {
  isLoading.value = true
  errorMessage.value = ''
  
  try {
    const response = await authAPI.login(credentials.value)
    
    if (response.data && response.data.token) {
      // 触发登录成功事件
      emit('login-success', response.data)
      // 关闭模态框
      closeModal(true)
    } else {
      throw new Error('登录响应格式不正确')
    }
  } catch (error) {
    console.error('登录失败', error)
    errorMessage.value = error.response?.data?.message || '登录失败，请检查用户名和密码'
  } finally {
    isLoading.value = false
  }
}

// 暴露方法给父组件
defineExpose({
  openModal
})
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-container {
  background-color: white;
  border-radius: 8px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.modal-header {
  padding: 16px 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.25rem;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #999;
  transition: color 0.2s;
}

.close-btn:hover {
  color: #333;
}

.modal-body {
  padding: 20px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #555;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-group input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.login-btn {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.login-btn:hover:not(:disabled) {
  background-color: #0056b3;
}

.login-btn:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.error-message {
  color: #dc3545;
  margin-bottom: 16px;
  padding: 8px;
  background-color: #f8d7da;
  border-radius: 4px;
  text-align: center;
}
</style>
