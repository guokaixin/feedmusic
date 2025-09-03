<template>
  <div class="news-page">
    <div class="container">
      <!-- 页面标题和新增按钮 -->
      <div class="page-header">
        <h1>新闻动态</h1>
        <button 
          class="add-news-btn" 
          @click="goToCreateNews"
          v-if="isAdmin"
        >
          新增新闻
        </button>
      </div>
      
      <!-- 未登录提示 -->
      <div v-if="!isAuthenticated" class="auth-required">
        <p>您尚未登录，请先登录后查看新闻内容。</p>
        <button class="login-prompt-btn" @click="openLoginModal">
          去登录
        </button>
      </div>
      
      <!-- 加载状态 -->
      <div v-if="isLoading && isAuthenticated" class="loading-state">
        <p>正在加载新闻数据...</p>
      </div>
      
      <!-- 错误状态 -->
      <div v-if="hasError && isAuthenticated" class="error-state">
        <p>数据加载失败，请稍后重试。</p>
        <button class="retry-btn" @click="loadNews(1, true)">
          重试
        </button>
      </div>
      
      <!-- 新闻列表 -->
      <div v-if="newsList.length > 0 && isAuthenticated" class="news-list">
        <div class="news-item" v-for="news in newsList" :key="news.id">
          <h2 class="news-title">{{ news.title }}</h2>
          
          <div class="news-image" v-if="news.image_url">
            <img :src="news.image_url" :alt="news.title">
          </div>
          
          <div class="news-content">
            <p>{{ news.description }}</p>
          </div>
          
          <div class="news-meta">
          <div class="news-author">
            创作者: {{ news.username || '未知用户' }}
          </div>
            <span>{{ formatDate(news.created_at) }}</span>
            <div class="news-actions" v-if="isAdmin">
              <button @click="goToEditNews(news.id)" class="edit-btn">编辑</button>
              <button @click="deleteNews(news.id)" class="delete-btn">删除</button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 空状态 -->
      <div v-if="newsList.length === 0 && !isLoading && !hasError && isAuthenticated" class="empty-state">
        <p>暂无新闻数据</p>
      </div>
      
      <!-- 分页控件 -->
      <div v-if="totalPages > 1 && isAuthenticated" class="pagination">
        <button 
          @click="changePage(currentPage - 1)" 
          :disabled="currentPage === 1"
        >
          上一页
        </button>
        
        <span class="page-info">
          第 {{ currentPage }} 页 / 共 {{ totalPages }} 页
        </span>
        
        <button 
          @click="changePage(currentPage + 1)" 
          :disabled="currentPage === totalPages"
        >
          下一页
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, inject } from 'vue'
import { useRouter } from 'vue-router'
import { newsAPI, adminAPI } from '../services/api'

const router = useRouter()
const openLoginModal = inject('openLoginModal', () => {
  router.push('/auth/login')
})

// 新闻数据
const newsList = ref([])
const currentPage = ref(1)
const perPage = ref(6)
const totalNews = ref(0)
const totalPages = ref(0)

// 状态管理
const isLoading = ref(false)
const hasError = ref(false)
const isAuthenticated = ref(false)
const isAdmin = ref(false)

// 检查登录状态
const checkAuthStatus = () => {
  try {
    const token = localStorage.getItem('token')
    const userData = localStorage.getItem('user')
    
    if (token && userData && userData !== 'undefined' && userData !== 'null') {
      isAuthenticated.value = true
      try {
        const user = JSON.parse(userData)
        isAdmin.value = user.role === 'admin' || user.role === 'Admin'
      } catch (e) {
        console.error('解析用户数据失败', e)
        isAdmin.value = false
      }
    } else {
      isAuthenticated.value = false
      isAdmin.value = false
    }
  } catch (error) {
    console.error('检查登录状态失败', error)
    isAuthenticated.value = false
    isAdmin.value = false
  }
}

// 加载新闻数据
const loadNews = async (page = 1, reset = false) => {
  if (!isAuthenticated.value) return
  
  if (reset) {
    newsList.value = []
    hasError.value = false
  }
  
  isLoading.value = true
  
  try {
    const response = await newsAPI.getNews(page, perPage.value)
    
    if (response.data && response.data.items) {
      newsList.value = response.data.items
      totalNews.value = response.data.total
      currentPage.value = response.data.page
      totalPages.value = response.data.pages
    } else {
      throw new Error('新闻数据格式不正确')
    }
  } catch (error) {
    console.error('加载新闻失败', error)
    hasError.value = true
  } finally {
    isLoading.value = false
  }
}

// 切换页码
const changePage = (page) => {
  if (page < 1 || page > totalPages.value) return
  currentPage.value = page
  loadNews(page)
  
  // 平滑滚动到页面顶部
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString()
}

// 跳转到新增新闻页面
const goToCreateNews = () => {
  console.log('尝试跳转到创建新闻页面')
  router.push({ name: 'CreateNews' })
}

// 跳转到编辑新闻页面
const goToEditNews = (id) => {
  router.push({ name: 'EditNews', params: { id } })
}

// 删除新闻
const deleteNews = async (id) => {
  if (!confirm('确定要删除这条新闻吗？')) return
  
  try {
    await adminAPI.deleteNews(id)
    loadNews(currentPage.value)
  } catch (error) {
    console.error('删除新闻失败', error)
    alert(error.response?.data?.message || '删除新闻失败，请重试')
  }
}

// 监听登录状态变化
watch(isAuthenticated, (newVal) => {
  if (newVal) {
    loadNews()
  }
})

// 页面挂载时检查登录状态
onMounted(() => {
  checkAuthStatus()
})
</script>

<style scoped>
.news-page {
  padding: 2rem 0;
  width: 100%;
  box-sizing: border-box;
  min-height: calc(100vh - 180px);
  /* 添加背景图样式 */
  background-image: url('/assets/presentation-background.jpg');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  background-repeat: no-repeat;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  /* 添加半透明白色背景以确保内容可读性 */
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 8px;
  padding: 2rem;
  margin-top: 2rem;
  margin-bottom: 2rem;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.add-news-btn {
  padding: 0.5rem 1rem;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.add-news-btn:hover {
  background-color: #218838;
}

.auth-required, .loading-state, .error-state, .empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 8px;
  margin-bottom: 2rem;
}

.auth-required p, .loading-state p, .error-state p, .empty-state p {
  font-size: 18px;
  color: #333;
  margin-bottom: 20px;
}

.login-prompt-btn, .retry-btn {
  padding: 8px 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.login-prompt-btn:hover, .retry-btn:hover {
  background-color: #0056b3;
}

.news-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.news-item {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.3s;
}

.news-item:hover {
  transform: translateY(-5px);
}

.news-title {
  font-size: 20px;
  margin: 0;
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
}

.news-image {
  width: 100%;
  height: 200px;
  overflow: hidden;
}

.news-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.news-image img:hover {
  transform: scale(1.05);
}

.news-content {
  padding: 20px;
}

.news-content p {
  margin: 0;
  color: #666;
  line-height: 1.6;
}

.news-meta {
  padding: 15px 20px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
  color: #999;
}

.news-actions {
  display: flex;
  gap: 10px;
}

.edit-btn, .delete-btn {
  padding: 5px 10px;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.edit-btn {
  background-color: #007bff;
  color: white;
}

.edit-btn:hover {
  background-color: #0056b3;
}

.delete-btn {
  background-color: #dc3545;
  color: white;
}

.delete-btn:hover {
  background-color: #bb2d3b;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
  margin-top: 20px;
  padding-bottom: 2rem;
}

.pagination button {
  padding: 8px 16px;
  background-color: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.pagination button:hover:not(:disabled) {
  background-color: #e9ecef;
  border-color: #ccc;
}

.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  color: #666;
}
</style>