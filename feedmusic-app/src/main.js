// src/main.js 正确写法
import { createApp } from 'vue'
import App from './App.vue'
import './style.css'
// 引入 router/index.js 中的路由配置
import router from './router'  

const app = createApp(App)
app.use(router)  // 使用完整路由表
app.mount('#app')