<template>
  <footer class="app-footer">
    <div class="container">
      <div class="footer-content">
        <p>&copy; {{ new Date().getFullYear() }} FeedMusic. 保留所有权利。</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
// 页脚组件
</script>

<style scoped>
.app-footer {
  background-color: #f8f9fa;
  padding: 2rem 0;
  margin-top: auto;
  width: 100%;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.footer-content {
  text-align: center;
  color: #6c757d;
}
</style>
