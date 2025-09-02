<template>
  <div class="admin-news-form">
    <div class="container">
      <h1>{{ isEditing ? '编辑新闻' : '创建新闻' }}</h1>
      
      <form @submit.prevent="handleSubmit" class="news-form">
        <div class="form-group">
          <label for="title">新闻标题</label>
          <input
            type="text"
            id="title"
            v-model="formData.title"
            required
            placeholder="请输入新闻标题"
          >
        </div>
        
        <div class="form-group">
          <label for="description">新闻内容</label>
          <textarea
            id="description"
            v-model="formData.description"
            required
            rows="6"
            placeholder="请输入新闻内容"
          ></textarea>
        </div>
        
        <div class="form-group">
          <label for="image">新闻图片</label>
          <input
            type="file"
            id="image"
            accept="image/*"
            @change="handleImageChange"
          >
          
          <div v-if="previewUrl" class="image-preview">
            <img :src="previewUrl" alt="预览图">
          </div>
        </div>
        
        <div class="form-actions">
          <button type="button" class="cancel-btn" @click="goBack">取消</button>
          <button type="submit" class="submit-btn" :disabled="isSubmitting">
            <span v-if="!isSubmitting">{{ isEditing ? '更新新闻' : '创建新闻' }}</span>
            <span v-if="isSubmitting">提交中...</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { adminAPI } from '../services/api'

const router = useRouter()
const route = useRoute()

// 判断是编辑还是创建
const isEditing = ref(!!route.params.id)
const isSubmitting = ref(false)
const formData = ref({
  title: '',
  description: ''
})
const selectedImage = ref(null)
const previewUrl = ref('')

// 加载要编辑的新闻数据
const loadNewsData = async () => {
  if (!isEditing.value) return
  
  try {
    const response = await adminAPI.getNewsById(route.params.id)
    if (response.data) {
      formData.value.title = response.data.title
      formData.value.description = response.data.description
      // 处理图片预览路径
      if (response.data.image) {
        // 兼容后端返回的图片路径格式
        previewUrl.value = `/assets/${response.data.image}`
      }
    } else {
      throw new Error('获取到空的新闻数据')
    }
  } catch (error) {
    console.error('加载新闻数据失败', error.response?.data || error.message)
    alert(`加载新闻数据失败: ${error.response?.data?.message || error.message}`)
    goBack()
  }
}

// 处理图片选择
const handleImageChange = (e) => {
  const file = e.target.files[0]
  if (file) {
    selectedImage.value = file
    // 显示预览
    previewUrl.value = URL.createObjectURL(file)
  }
}

// 表单提交
const handleSubmit = async () => {
  isSubmitting.value = true
  
  try {
    // 创建FormData对象
    const form = new FormData()
    form.append('title', formData.value.title)
    form.append('description', formData.value.description)
    
    // 如果有选择图片，添加到FormData
    if (selectedImage.value) {
      form.append('image', selectedImage.value)
    }
    
    if (isEditing.value) {
      // 编辑新闻
      await adminAPI.updateNews(route.params.id, form)
      alert('新闻更新成功')
    } else {
      // 创建新闻
      await adminAPI.createNews(form)
      alert('新闻创建成功')
    }
    
    // 提交成功后返回新闻列表
    router.push({ name: 'News' })
  } catch (error) {
    console.error('提交新闻失败', error)
    alert(error.response?.data?.message || '提交失败，请重试')
  } finally {
    isSubmitting.value = false
  }
}

// 返回新闻列表
const goBack = () => {
  router.push({ name: 'News' })
}

// 页面挂载时加载数据
onMounted(() => {
  loadNewsData()
})
</script>

<style scoped>
.admin-news-form {
  padding: 2rem 0;
  max-width: 800px;
  margin: 0 auto;
  width: 100%;
  box-sizing: border-box;
}

h1 {
  margin-bottom: 2rem;
  color: #333;
}

.news-form {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #555;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  box-sizing: border-box;
}

.form-group textarea {
  resize: vertical;
}

.image-preview {
  margin-top: 1rem;
  max-width: 300px;
}

.image-preview img {
  width: 100%;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}

.cancel-btn, .submit-btn {
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  font-size: 1rem;
}

.cancel-btn {
  background-color: #6c757d;
  color: white;
}

.cancel-btn:hover {
  background-color: #5a6268;
}

.submit-btn {
  background-color: #28a745;
  color: white;
}

.submit-btn:hover:not(:disabled) {
  background-color: #218838;
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style>