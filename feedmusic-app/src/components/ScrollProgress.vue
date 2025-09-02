<template>
  <div class="scroll-progress" :style="{ width: progress + '%' }"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'

const progress = ref(0)
const router = useRouter()

// 根据当前路由更新进度条
const updateProgressFromRoute = () => {
  const currentRoute = router.currentRoute.value.name
  progress.value = currentRoute === 'Introduction' ? 0 : 100
}

// 处理滚动事件更新进度条
const handleScroll = () => {
  const scrollPosition = window.scrollY
  const windowHeight = window.innerHeight
  
  // 计算进度百分比
  let newProgress = (scrollPosition / windowHeight) * 100
  
  // 限制在0-100之间
  newProgress = Math.max(0, Math.min(100, newProgress))
  
  // 如果滚动超过50%，切换到下一页
  if (newProgress > 50 && router.currentRoute.value.name === 'Introduction') {
    router.push({ name: 'News' })
  } else if (newProgress < 50 && router.currentRoute.value.name === 'News') {
    router.push({ name: 'Introduction' })
  }
  
  progress.value = newProgress
}

onMounted(() => {
  // 初始化进度条
  updateProgressFromRoute()
  
  // 监听路由变化
  router.afterEach(updateProgressFromRoute)
  
  // 监听滚动事件
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>
