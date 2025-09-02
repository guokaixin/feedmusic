from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import News, User
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from app import db
from app.utils import get_file_url  # 导入工具函数

news_bp = Blueprint('news', __name__)

# 允许的图片扩展名
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@news_bp.route('/news', methods=['GET'])
@jwt_required()
def get_news():
    """获取新闻列表，支持分页"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 6, type=int)
    
    if per_page > 20:
        per_page = 20
    
    pagination = News.query.order_by(News.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    news_items = []
    for news in pagination.items:
        author = User.query.get(news.author_id)
        username = author.username if author else "未知用户"
        news_items.append({
            'id': news.id,
            'title': news.title,
            'description': news.description,
            'image_url': get_file_url(news.image_url),  # 生成完整URL
            'created_at': news.created_at.isoformat(),
            'username': username
        })
    
    return jsonify({
        'items': news_items,
        'page': pagination.page,
        'per_page': pagination.per_page,
        'total': pagination.total,
        'pages': pagination.pages
    }), 200

@news_bp.route('/news/<int:id>', methods=['GET'])
@jwt_required()
def get_news_by_id(id):
    """根据ID获取新闻详情"""
    news = News.query.get_or_404(id)
    author = User.query.get(news.author_id)
    username = author.username if author else "未知用户"
    

    return jsonify({
        'id': news.id,
        'title': news.title,
        'description': news.description,
        'username': username,
        'image_url': get_file_url(news.image_url),  # 生成完整URL
        'created_at': news.created_at.isoformat()
    }), 200

@news_bp.route('/admin/news', methods=['POST'])
@jwt_required()
def create_news():
    """创建新闻（与admin蓝图保持一致）"""
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    
    if user.role != 'admin':
        return jsonify({"message": "没有权限创建新闻"}), 403
    
    title = request.form.get('title')
    description = request.form.get('description')
    
    if not title or not description:
        return jsonify({"message": "标题和内容为必填项"}), 400
    
    image_url = None
    if 'image' in request.files:
        file = request.files['image']
        if file and allowed_file(file.filename):
            upload_folder = current_app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)
            
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            filename = f"{timestamp}_{filename}"
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            
            image_url = f'/static/uploads/{filename}'
    
    news = News(
        title=title,
        description=description,
        image_url=image_url,
        author_id=user_id  # 修正字段名（原代码用了created_by，数据库中是author_id）
    )
    
    db.session.add(news)
    db.session.commit()
    
    return jsonify({
        "message": "新闻创建成功",
        "id": news.id,
        "image_url": get_file_url(image_url)
    }), 201

@news_bp.route('/admin/news/<int:id>', methods=['PUT'])
@jwt_required()
def update_news(id):
    """更新新闻"""
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    
    if user.role != 'admin':
        return jsonify({"message": "没有权限更新新闻"}), 403
    
    news = News.query.get_or_404(id)
    
    title = request.form.get('title')
    description = request.form.get('description')
    
    if not title or not description:
        return jsonify({"message": "标题和内容为必填项"}), 400
    
    news.title = title
    news.description = description
    
    if 'image' in request.files:
        file = request.files['image']
        if file and allowed_file(file.filename):
            # 删除旧图片
            if news.image_url and news.image_url.startswith('/static/uploads/'):
                old_path = os.path.join(current_app.root_path, news.image_url.lstrip('/'))
                if os.path.exists(old_path):
                    os.remove(old_path)
            
            # 保存新图片
            upload_folder = current_app.config['UPLOAD_FOLDER']
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            filename = f"{timestamp}_{filename}"
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            
            news.image_url = f'/static/uploads/{filename}'
    
    db.session.commit()
    
    return jsonify({"message": "新闻更新成功"}), 200

@news_bp.route('/admin/news/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_news(id):
    """删除新闻"""
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    
    if user.role != 'admin':
        return jsonify({"message": "没有权限删除新闻"}), 403
    
    news = News.query.get_or_404(id)
    
    # 删除图片
    if news.image_url and news.image_url.startswith('/static/uploads/'):
        file_path = os.path.join(current_app.root_path, news.image_url.lstrip('/'))
        if os.path.exists(file_path):
            os.remove(file_path)
    
    db.session.delete(news)
    db.session.commit()
    
    return jsonify({"message": "新闻删除成功"}), 200