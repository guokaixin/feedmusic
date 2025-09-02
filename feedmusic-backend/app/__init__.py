from flask import Flask, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
import os
from datetime import timedelta

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address)

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    # 动态获取当前请求的根路径
    @app.context_processor
    def inject_base_url():
        if request:
            return {'base_url': request.root_url.rstrip('/')}
        return {'base_url': ''}
    
    # 配置项 - 统一使用static/uploads路径
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-key-for-development-only'),
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'sqlite:///feedmusic.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key'),
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=24),
        UPLOAD_FOLDER=os.path.join(app.root_path, 'static', 'uploads'),  # 关键修改：统一为static/uploads
        ALLOWED_EXTENSIONS={'png', 'jpg', 'jpeg', 'gif'},
        MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB
        BASE_URL=os.environ.get('BASE_URL', 'http://localhost:5005')
    )
    
    # 确保上传文件夹存在
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    # 初始化扩展
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    limiter.init_app(app)
    
    # 注册蓝图
    from .routes.auth import auth_bp
    from .routes.news import news_bp
    from .routes.admin import admin_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(news_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    
    # 静态文件访问路由 - 只保留static/uploads的路由
    @app.route('/static/uploads/<path:filename>')
    def static_uploaded_file(filename):
        # 验证文件是否存在
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(file_path):
            return {"message": "文件不存在"}, 404
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
    return app