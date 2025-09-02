from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from werkzeug.utils import secure_filename
import os
from ..models import News, User
from .. import db
from ..utils import handle_file_upload, get_file_url  # 导入工具函数

admin_bp = Blueprint('admin', __name__)

# 创建新闻
@admin_bp.route('/news', methods=['POST'])
@jwt_required()
def create_news():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    # 获取表单数据
    title = request.form.get('title')
    description = request.form.get('description')
    
    # 验证必填字段
    if not title or not description:
        return jsonify({"message": "Missing required fields"}), 400
    
    # 处理文件上传（使用工具函数）
    image_url = None
    if 'image' in request.files:
        image_url = handle_file_upload(request.files['image'], user_id)
        if not image_url:
            return jsonify({"message": "Invalid image type"}), 400
    
    # 创建新闻
    news = News(
        title=title,
        description=description,
        image_url=image_url,
        author_id=user_id
    )
    
    db.session.add(news)
    db.session.commit()
    
    return jsonify({
        "id": news.id,
        "message": "News created successfully",
        "image_url": get_file_url(image_url)  # 返回完整URL
    }), 201

# 更新新闻
@admin_bp.route('/news/<int:id>', methods=['PUT'])
@jwt_required()
def update_news(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    news = News.query.get_or_404(id)
    
    # 检查权限
    if news.author_id != user_id and user.role != 'admin':
        return jsonify({"message": "Permission denied"}), 403
    
    # 获取表单数据
    title = request.form.get('title')
    description = request.form.get('description')
    
    # 更新字段
    if title:
        news.title = title
    if description:
        news.description = description
    
    # 处理文件上传（使用工具函数）
    if 'image' in request.files:
        # 删除旧图片
        if news.image_url and news.image_url.startswith('/static/uploads/'):
            old_filename = news.image_url.split('/')[-1]
            old_filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], old_filename)
            if os.path.exists(old_filepath):
                os.remove(old_filepath)
        
        # 保存新图片
        new_image_url = handle_file_upload(request.files['image'], user_id)
        if new_image_url:
            news.image_url = new_image_url
        else:
            return jsonify({"message": "Invalid image type"}), 400
    
    db.session.commit()
    
    return jsonify({"message": "News updated successfully"}), 200

# 删除新闻
@admin_bp.route('/news/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_news(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    news = News.query.get_or_404(id)
    
    # 检查权限
    if news.author_id != user_id and user.role != 'admin':
        return jsonify({"message": "Permission denied"}), 403
    
    # 删除图片文件
    if news.image_url and news.image_url.startswith('/static/uploads/'):
        filename = news.image_url.split('/')[-1]
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(filepath):
            os.remove(filepath)
    
    db.session.delete(news)
    db.session.commit()
    
    return jsonify({"message": "News deleted successfully"}), 200

# 获取我的新闻
@admin_bp.route('/news', methods=['GET'])
@jwt_required()
def get_my_news():
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    pagination = News.query.filter_by(author_id=user_id).order_by(News.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
        # 获取当前用户信息
    current_user = User.query.get(user_id)
    username = current_user.username if current_user else "未知用户"
    result = {
        "items": [
            {
                "id": item.id,
                "title": item.title,
                "description": item.description,
                "username": username,
                "image_url": get_file_url(item.image_url),  # 使用工具函数生成完整URL
                "created_at": item.created_at.isoformat()
            } for item in pagination.items
        ],
        "total": pagination.total,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "pages": pagination.pages
    }
    
    return jsonify(result), 200

# 获取所有用户（仅管理员）
@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    # 检查是否为管理员
    user = User.query.get(get_jwt_identity())
    if user.role != 'admin':
        return jsonify({"message": "Admin required"}), 403
    
    users = User.query.all()
    
    return jsonify([
        {
            "id": user.id,
            "username": user.username,
            "role": user.role,
            "created_at": user.created_at.isoformat()
        } for user in users
    ]), 200