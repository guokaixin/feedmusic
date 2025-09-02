import axios from 'axios'
import router from '../router'

// 创建axios实例
const api = axios.create({
  baseURL: (import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000') + '/api',
  timeout: 5000
})

// 请求拦截器 - 添加认证token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// 响应拦截器 - 处理认证错误
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // 处理401未授权错误
    if (error.response && error.response.status === 401) {
      // 清除本地存储的认证信息
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      
      // 如果当前不在首页，重定向到首页
      if (router.currentRoute.value.name !== 'Introduction') {
        router.push('/')
      }
    }
    return Promise.reject(error)
  }
)

// 认证相关API
export const authAPI = {
  login: (credentials) => api.post('/login', credentials), // 修正登录接口路径
  logout: () => api.post('/logout'),
  getCurrentUser: () => api.get('/auth/me')
}

// 新闻相关API
export const newsAPI = {
  getNews: (page = 1, perPage = 6) => api.get(`/news?page=${page}&per_page=${perPage}`),
  getNewsById: (id) => api.get(`/news/${id}`)
}

// 管理员相关API
export const adminAPI = {
  createNews: (newsData) => {
    const config = {
      headers: { 'Content-Type': 'multipart/form-data' }
    }
    return api.post('/admin/news', newsData, config)
  },
  getMyNews: (page = 1, perPage = 10) => api.get(`/admin/news?page=${page}&per_page=${perPage}`),
  getNewsById: (id) => api.get(`/news/${id}`), // 添加此方法用于获取单条新闻
  updateNews: (id, newsData) => {
    const config = {
      headers: { 'Content-Type': 'multipart/form-data' }
    }
    return api.put(`/admin/news/${id}`, newsData, config)
  },
  deleteNews: (id) => api.delete(`/admin/news/${id}`)
}

export default api