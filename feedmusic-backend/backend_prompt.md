# 后端项目开发提示词

## 1. 技术栈与项目架构
- 使用Flask 2.0.1框架搭建后端，采用蓝图（Blueprint）划分路由模块（auth、news、admin）
- 集成指定版本依赖：Flask-SQLAlchemy 2.5.1（数据库ORM）、Flask-Migrate 3.1.0（数据库迁移）、Flask-JWT-Extended 4.3.1（JWT认证）、Flask-Limiter 2.0.2（限流）、python-dotenv 0.19.0（环境变量）、Werkzeug 2.0.1（工具库）
- 项目结构需包含：主程序入口（run.py）、应用初始化模块（app/__init__.py）、路由模块（app/routes/）、数据模型（app/models.py）、工具函数（app/utils.py）、数据库迁移文件（migrations/）

## 2. 数据库设计
- 设计User模型：包含id（主键）、username（唯一）、password_hash（密码哈希）、role（角色：user/admin）、created_at（创建时间），实现set_password（加密）和check_password（验证）方法
- 设计News模型：包含id（主键）、title（标题）、description（内容）、image_url（图片路径）、created_at（创建时间）、author_id（外键关联User）
- 使用Flask-Migrate生成迁移脚本，初始版本需包含用户表和新闻表

## 3. 认证与权限
- 基于JWT实现认证：登录接口（验证用户名密码生成令牌，有效期7天）、登出接口（客户端删除令牌）、获取当前用户信息接口
- 权限控制：管理员可操作所有资源，普通用户仅能操作自己创建的内容
- 所有需要权限的接口需添加@jwt_required()装饰器

## 4. 核心功能模块
### 新闻管理
- 实现新闻CRUD接口：
  - 创建：支持标题、内容、图片上传（格式限制：png/jpg/jpeg/gif，大小≤16MB）
  - 更新：支持修改标题、内容，重新上传图片时删除旧图
  - 删除：同时删除关联图片文件
  - 查询：列表支持分页（默认每页10条，新闻表默认6条）、按创建时间倒序，详情包含作者信息
- 区分管理员与普通用户操作权限

### 文件上传
- 工具函数需实现：文件格式验证、生成包含用户ID和时间戳的唯一文件名、保存至static/uploads目录、生成完整访问URL
- 静态文件路由仅允许访问static/uploads目录，不存在的文件返回404

### 管理员功能
- 管理员专属接口：获取所有用户列表（包含ID、用户名、角色、创建时间）
- 管理员可创建/更新/删除任何用户的新闻

## 5. 配置与辅助功能
- 配置支持环境变量和默认值：数据库连接、JWT密钥、文件上传路径、BASE_URL等
- 实现CLI命令：init-db（清空数据并创建新表）、create-admin（创建默认管理员用户：admin/123456）
- 配置跨域支持（CORS）和接口限流
- 应用启动默认端口5005，支持debug模式