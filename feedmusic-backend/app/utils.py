import os
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import current_app

def allowed_file(filename):
    """检查文件是否允许上传"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'gif'})

def get_file_url(relative_path):
    """生成完整的文件访问URL"""
    if not relative_path:
        return None
    base_url = current_app.config.get('BASE_URL', 'http://localhost:5005').rstrip('/')
    relative_path = relative_path.lstrip('/')
    return f"{base_url}/{relative_path}"

def handle_file_upload(file, user_id):
    """处理文件上传并返回相对路径（统一为static/uploads）"""
    if not file or not allowed_file(file.filename):
        return None
        
    # 上传目录使用配置中的static/uploads
    upload_folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)
    
    # 生成安全的文件名
    filename = secure_filename(file.filename)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"{user_id}_{timestamp}_{filename}"  # 包含用户ID和时间戳确保唯一
    file_path = os.path.join(upload_folder, filename)
    
    # 保存文件
    file.save(file_path)
    
    # 返回相对路径（static/uploads开头）
    return f"/static/uploads/{filename}"