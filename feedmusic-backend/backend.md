FeedMusic 后端运行指南
本地运行（Conda 环境）
1. 环境准备
bash
# 创建并激活 Conda 环境
conda create -n feedmusic python=3.8
conda activate feedmusic

 **下载项目**
   ```bash
   git clone git@github.com:guokaixin/feedmusic.git
   cd feedmusic/feedmusic-backend
   ```

# 安装依赖
pip install -r requirements.txt
2. 配置环境变量（可选）
创建 .env 文件，添加以下内容（根据需要修改）：
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret
DATABASE_URL=sqlite:///feedmusic.db
BASE_URL=http://localhost:5005

3. 初始化数据库
bash
# 初始化数据库
flask init-db

# 创建管理员用户（用户名: admin, 密码: 123456）
flask create-admin
4. 启动应用
bash
# 直接运行
python run.py

# 或使用 Flask 命令
flask run --host=0.0.0.0 --port=5005
应用将在 http://localhost:5005 启动
Docker 运行
1. 创建 Dockerfile
在项目根目录创建 Dockerfile：
dockerfile
FROM python:3.8-slim

WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 创建数据目录和上传目录
RUN mkdir -p instance static/uploads

# 暴露端口
EXPOSE 5005

# 初始化数据库并启动应用
CMD ["sh", "-c", "flask init-db && flask create-admin && python run.py"]
2. 构建 Docker 镜像
bash
docker build -t feedmusic-backend .
3. 运行 Docker 容器
bash
# 基本运行
docker run -d -p 5005:5005 --name feedmusic-api feedmusic-backend

# 持久化数据（推荐）
docker run -d \
  -p 5005:5005 \
  -v $(pwd)/instance:/app/instance \
  -v $(pwd)/static/uploads:/app/static/uploads \
  --name feedmusic-api \
  feedmusic-backend
4. 环境变量配置（可选）
如需自定义配置，可以在运行时添加环境变量：
bash
docker run -d \
  -p 5005:5005 \
  -e SECRET_KEY=your_secret_key \
  -e JWT_SECRET_KEY=your_jwt_secret \
  -e BASE_URL=http://your-domain:5005 \
  -v $(pwd)/instance:/app/instance \
  -v $(pwd)/static/uploads:/app/static/uploads \
  --name feedmusic-api \
  feedmusic-backend
验证运行状态
启动后，可通过以下方式验证服务是否正常：
bash
# 检查服务是否启动
curl http://localhost:5005/api/auth/me

# 预期返回（未登录状态）：{"msg":"Missing Authorization Header"}