<template>
  <div class="news-card">
    <div class="news-image-container">
      <img 
        :src="`/assets/${newsItem.image}`" 
        :alt="newsItem.title" 
        class="news-image"
      >
    </div>
    <div class="news-content">
      <h3 class="news-title">{{ newsItem.title }}</h3>
      <p class="news-description">{{ truncatedDescription }}</p>
      <div class="news-author">By: {{ newsItem.author }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  newsItem: {
    type: Object,
    required: true,
    default: () => ({
      title: '',
      description: '',
      image: '',
      author: ''
    })
  }
})

// 截断描述为两行
const truncatedDescription = computed(() => {
  const words = props.newsItem.description.split(' ')
  if (words.length <= 20) { // 大约两行的字数
    return props.newsItem.description
  }
  return words.slice(0, 20).join(' ') + '...'
})
</script>

<style scoped>
.news-card {
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.news-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.news-image-container {
  height: 200px;
  overflow: hidden;
}

.news-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.news-card:hover .news-image {
  transform: scale(1.05);
}

.news-content {
  padding: 20px;
}

.news-title {
  font-size: 18px;
  margin-bottom: 10px;
  font-weight: bold;
}

.news-description {
  font-size: 14px;
  color: #666;
  margin-bottom: 15px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  height: 40px;
}

.news-author {
  font-size: 12px;
  color: #999;
}
</style>
