# FeedMusic 前端应用

## 项目概述

FeedMusic 是一个基于 Vue 3 + Vite 的现代化音乐应用前端，提供新闻浏览、用户认证、管理后台等功能。

## 技术栈

- **前端框架**: Vue 3.4.31
- **构建工具**: Vite 5.2.11
- **路由**: Vue Router 4.3.2
- **HTTP客户端**: Axios 1.7.2
- **开发服务器**: Express 4.19.2
- **Node.js版本**: 20.19.4
- **npm版本**: 10.8.2

## 项目结构

```
feedmusic-app/
├── public/                 # 静态资源
│   └── assets/            # 图片、视频等资源
├── src/                   # 源代码
│   ├── components/        # Vue组件
│   │   ├── Footer.vue
│   │   ├── Header.vue
│   │   ├── LoginModal.vue
│   │   ├── Navbar.vue
│   │   ├── NewsCard.vue
│   │   └── ScrollProgress.vue
│   ├── views/             # 页面组件
│   │   ├── AdminNewsForm.vue
│   │   ├── Introduction.vue
│   │   └── News.vue
│   ├── router/            # 路由配置
│   │   └── index.js
│   ├── services/          # API服务
│   │   └── api.js
│   ├── App.vue            # 根组件
│   ├── main.js            # 入口文件
│   └── style.css          # 全局样式
├── server/                # 开发服务器
│   └── index.js           # Express服务器
├── index.html             # HTML模板
├── package.json           # 项目配置
├── vite.config.js         # Vite配置
└── README.md              # 项目文档
```

## 本地开发环境搭建

### 环境要求

- Node.js >= 20.19.4
- npm >= 10.8.2
- 现代浏览器（Chrome、Firefox、Safari、Edge）

### 安装步骤

1. **下载项目**
   ```bash
   git clone git@github.com:guokaixin/feedmusic.git
   cd feedmusic/feedmusic-app
   ```

2. **安装依赖**
   ```bash
   npm install
   ```

3. **启动开发服务器**
   ```bash
   npm run dev
   ```

   这个命令会同时启动：
   - Vite开发服务器（端口3000）
   - Express API服务器（端口5005）

4. **访问应用**
   - 前端应用: http://localhost:3000
   - API服务器: http://localhost:5005

### 可用脚本

```bash
# 开发模式（同时启动前端和后端）
npm run dev

# 仅启动前端开发服务器
npm run vite

# 仅启动后端API服务器
npm run server

# 构建生产版本
npm run build

# 预览生产构建
npm run preview
```

### 开发环境配置

项目使用环境变量进行配置，可以在根目录创建 `.env` 文件：

```env
# API基础URL
VITE_API_BASE_URL=http://localhost:5005

# 开发模式
NODE_ENV=development
```

## Docker 部署

### 方法一：使用 Dockerfile

1. **创建 Dockerfile**
   
   在 `feedmusic-app` 目录下创建 `Dockerfile`：

   ```dockerfile
   # 使用官方 Node.js 20 镜像
   FROM node:20.19.4-alpine

   # 设置工作目录
   WORKDIR /app

   # 复制 package.json 和 package-lock.json
   COPY package*.json ./

   # 安装依赖
   RUN npm ci --only=production

   # 复制源代码
   COPY . .

   # 构建应用
   RUN npm run build

   # 安装生产依赖（包括Express服务器）
   RUN npm install express cors

   # 暴露端口
   EXPOSE 3000

   # 启动应用
   CMD ["npm", "run", "preview"]
   ```

2. **构建Docker镜像**
   ```bash
   docker build -t feedmusic-frontend .
   ```

3. **运行容器**
   ```bash
   docker run -p 3000:3000 feedmusic-frontend
   ```

### 方法二：使用 Docker Compose（推荐）

1. **创建 docker-compose.yml**
   
   在项目根目录创建 `docker-compose.yml`：

   ```yaml
   version: '3.8'

   services:
     frontend:
       build:
         context: ./feedmusic-app
         dockerfile: Dockerfile
       ports:
         - "3000:3000"
       environment:
         - NODE_ENV=production
         - VITE_API_BASE_URL=http://backend:5005
       depends_on:
         - backend
       networks:
         - feedmusic-network

     backend:
       build:
         context: ./feedmusic-backend
         dockerfile: Dockerfile
       ports:
         - "5005:5005"
       environment:
         - FLASK_ENV=production
       networks:
         - feedmusic-network

   networks:
     feedmusic-network:
       driver: bridge
   ```

2. **创建优化的 Dockerfile**
   
   在 `feedmusic-app` 目录下创建 `Dockerfile`：

   ```dockerfile
   # 多阶段构建
   FROM node:20.19.4-alpine AS builder

   # 设置工作目录
   WORKDIR /app

   # 复制 package 文件
   COPY package*.json ./

   # 安装所有依赖（包括开发依赖）
   RUN npm ci

   # 复制源代码
   COPY . .

   # 构建应用
   RUN npm run build

   # 生产阶段
   FROM node:20.19.4-alpine AS production

   # 设置工作目录
   WORKDIR /app

   # 复制 package 文件
   COPY package*.json ./

   # 只安装生产依赖
   RUN npm ci --only=production && npm cache clean --force

   # 从构建阶段复制构建结果
   COPY --from=builder /app/dist ./dist
   COPY --from=builder /app/server ./server

   # 创建非root用户
   RUN addgroup -g 1001 -S nodejs
   RUN adduser -S nextjs -u 1001

   # 更改文件所有权
   RUN chown -R nextjs:nodejs /app
   USER nextjs

   # 暴露端口
   EXPOSE 3000

   # 健康检查
   HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
     CMD curl -f http://localhost:3000 || exit 1

   # 启动应用
   CMD ["node", "server/index.js"]
   ```

3. **启动服务**
   ```bash
   # 构建并启动所有服务
   docker-compose up --build

   # 后台运行
   docker-compose up -d --build

   # 查看日志
   docker-compose logs -f

   # 停止服务
   docker-compose down
   ```

### 方法三：仅前端Docker部署

如果只需要部署前端，可以使用以下配置：

1. **创建简化的 Dockerfile**
   ```dockerfile
   FROM node:20.19.4-alpine

   WORKDIR /app

   # 复制依赖文件
   COPY package*.json ./

   # 安装依赖
   RUN npm ci

   # 复制源代码
   COPY . .

   # 构建应用
   RUN npm run build

   # 使用 nginx 提供静态文件服务
   FROM nginx:alpine
   COPY --from=0 /app/dist /usr/share/nginx/html
   COPY nginx.conf /etc/nginx/nginx.conf

   EXPOSE 80
   CMD ["nginx", "-g", "daemon off;"]
   ```

2. **创建 nginx.conf**
   ```nginx
   events {
       worker_connections 1024;
   }

   http {
       include       /etc/nginx/mime.types;
       default_type  application/octet-stream;

       server {
           listen 80;
           server_name localhost;
           root /usr/share/nginx/html;
           index index.html;

           location / {
               try_files $uri $uri/ /index.html;
           }

           location /api {
               proxy_pass http://backend:5005;
               proxy_set_header Host $host;
               proxy_set_header X-Real-IP $remote_addr;
           }
       }
   }
   ```

## 环境变量配置

### 开发环境
```env
# .env.development
VITE_API_BASE_URL=http://localhost:5005
NODE_ENV=development
```

### 生产环境
```env
# .env.production
VITE_API_BASE_URL=http://your-backend-domain.com
NODE_ENV=production
```

## 常见问题解决

### 1. 端口冲突
如果端口3000或5005被占用，可以修改配置：

**修改 vite.config.js:**
```javascript
server: {
  port: 3001, // 改为其他端口
  // ...
}
```

**修改 server/index.js:**
```javascript
const port = 5006; // 改为其他端口
```

### 2. 依赖安装失败
```bash
# 清除缓存
npm cache clean --force

# 删除 node_modules 重新安装
rm -rf node_modules package-lock.json
npm install
```

### 3. Docker构建失败
```bash
# 清除Docker缓存
docker system prune -a

# 重新构建
docker build --no-cache -t feedmusic-frontend .
```

### 4. 跨域问题
开发环境下，Vite已配置代理解决跨域问题。生产环境需要确保后端CORS配置正确。

## 部署到生产环境

### 1. 构建生产版本
```bash
npm run build
```

### 2. 使用Docker部署
```bash
# 构建镜像
docker build -t feedmusic-frontend:latest .

# 运行容器
docker run -d -p 3000:3000 --name feedmusic-app feedmusic-frontend:latest
```

### 3. 使用Docker Compose部署
```bash
# 生产环境部署
docker-compose -f docker-compose.prod.yml up -d
```

## 监控和日志

### 查看应用日志
```bash
# Docker容器日志
docker logs feedmusic-app

# Docker Compose日志
docker-compose logs -f frontend
```

### 健康检查
应用提供健康检查端点：
- 前端: http://localhost:3000
- API: http://localhost:5005/api/health

## 开发指南

### 添加新功能
1. 在 `src/components/` 中创建新组件
2. 在 `src/views/` 中创建新页面
3. 在 `src/router/index.js` 中添加路由
4. 在 `src/services/api.js` 中添加API调用

### 代码规范
- 使用ES6+语法
- 组件名使用PascalCase
- 文件名使用kebab-case
- 使用Vue 3 Composition API

## 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request
