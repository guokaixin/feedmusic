<template>
  <div class="introduction-page page">
    <!-- 视频背景 -->
    <div class="video-background">
      <video 
        src="/assets/intro.mp4" 
        autoplay 
        muted 
        loop 
        playsinline
        class="background-video"
      ></video>
      <div class="video-overlay"></div>
    </div>
    
    <!-- 文字内容 -->
    <div class="content">
      <h1 class="main-title">FeedMusic</h1>
      <p class="subtitle">发现、分享和享受音乐的新方式</p>
    </div>
    
    <!-- 滚动提示 -->
    <div class="scroll-indicator" @click="scrollToNews">
      <span>向下滚动</span>
      <div class="chevron"></div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const titleRef = ref(null);

// 滚动到新闻页面
const scrollToNews = () => {
  router.push({ name: 'News' });
};

// 文字动画效果
onMounted(() => {
  // 可以在这里添加文字滚动动画
  const animateText = () => {
    const titles = document.querySelectorAll('.main-title, .subtitle');
    titles.forEach((title, index) => {
      setTimeout(() => {
        title.style.opacity = '1';
        title.style.transform = 'translateY(0)';
      }, 300 * (index + 1));
    });
  };
  
  animateText();
});
</script>

<style scoped>
.introduction-page {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.video-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: 0;
}

.background-video {
  min-width: 100%;
  min-height: 100%;
  object-fit: cover;
}

.video-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
}

.content {
  position: relative;
  z-index: 1;
  padding: 20px;
}

.main-title {
  font-size: 5rem;
  color: white;
  margin-bottom: 20px;
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 1s ease, transform 1s ease;
}

.subtitle {
  font-size: 1.5rem;
  color: white;
  max-width: 700px;
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 1s ease 0.3s, transform 1s ease 0.3s;
}

/* 滚动指示器 */
.scroll-indicator {
  position: absolute;
  bottom: 50px;
  left: 50%;
  transform: translateX(-50%);
  color: white;
  cursor: pointer;
  z-index: 1;
  text-align: center;
}

.scroll-indicator span {
  display: block;
  margin-bottom: 10px;
  font-size: 14px;
}

.chevron {
  width: 24px;
  height: 24px;
  border: 2px solid white;
  border-radius: 50%;
  position: relative;
  animation: bounce 2s infinite;
}

.chevron::after {
  content: '';
  position: absolute;
  top: 8px;
  left: 6px;
  width: 8px;
  height: 8px;
  border-bottom: 2px solid white;
  border-right: 2px solid white;
  transform: rotate(45deg);
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateX(-50%) translateY(0);
  }
  40% {
    transform: translateX(-50%) translateY(-20px);
  }
  60% {
    transform: translateX(-50%) translateY(-10px);
  }
}

/* 响应式调整 */
@media (max-width: 768px) {
  .main-title {
    font-size: 3rem;
  }
  
  .subtitle {
    font-size: 1.2rem;
  }
}
</style>