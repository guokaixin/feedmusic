from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from app.models import User
import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"message": "请提供用户名和密码"}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({"message": "用户名或密码不正确"}), 401
    
    # 创建令牌，有效期设置为7天
    access_token = create_access_token(
        identity=user.id,
        expires_delta=datetime.timedelta(days=7)
    )
    
    return jsonify({
        "message": "登录成功",
        "token": access_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role
        }
    }), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # 在无状态JWT认证中，客户端登出只需客户端删除token即可
    # 这里仅作为示例，实际应用可能需要维护黑名单
    return jsonify({"message": "成功登出"}), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """获取当前登录用户信息"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"message": "用户不存在"}), 404
    
    return jsonify({
        "id": user.id,
        "username": user.username,
        "role": user.role
    }), 200
