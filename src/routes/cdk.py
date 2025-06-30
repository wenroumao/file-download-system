from flask import Blueprint, request, jsonify, send_file, current_app
from src.models.cdk import CDK, db
import os
import secrets
import string
from datetime import datetime

cdk_bp = Blueprint('cdk', __name__)

def generate_cdk_code():
    """生成随机CDK码"""
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(16))

@cdk_bp.route('/verify_cdk', methods=['POST'])
def verify_cdk():
    """验证CDK并绑定设备"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': '请求数据格式错误'}), 400
        
        cdk_code = data.get('cdk', '').strip().upper()
        device_id = data.get('device_id', '').strip()
        
        if not cdk_code or not device_id:
            return jsonify({'status': 'error', 'message': 'CDK和设备ID不能为空'}), 400
        
        # 验证CDK
        is_valid, message = CDK.verify_cdk(cdk_code, device_id)
        
        if is_valid:
            return jsonify({
                'status': 'success',
                'message': message,
                'download_url': '/api/download_file'
            }), 200
        else:
            return jsonify({'status': 'error', 'message': message}), 400
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'服务器错误: {str(e)}'}), 500

@cdk_bp.route('/download_file', methods=['GET'])
def download_file():
    """下载文件"""
    try:
        device_id = request.headers.get('Device-ID', '').strip()
        
        if not device_id:
            return jsonify({'status': 'error', 'message': '缺少设备ID'}), 400
        
        # 检查设备是否已授权
        if not CDK.is_device_authorized(device_id):
            return jsonify({'status': 'error', 'message': '设备未授权'}), 403
        
        # 查找压缩文件
        files_dir = os.path.join(current_app.root_path, 'files')
        if not os.path.exists(files_dir):
            return jsonify({'status': 'error', 'message': '文件目录不存在'}), 404
        
        # 查找第一个压缩文件
        for filename in os.listdir(files_dir):
            if filename.lower().endswith(('.zip', '.rar', '.7z', '.tar.gz')):
                file_path = os.path.join(files_dir, filename)
                return send_file(file_path, as_attachment=True, download_name=filename)
        
        return jsonify({'status': 'error', 'message': '未找到可下载的文件'}), 404
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'服务器错误: {str(e)}'}), 500

@cdk_bp.route('/generate_cdk', methods=['POST'])
def generate_cdk():
    """生成CDK（管理员功能）"""
    try:
        data = request.get_json()
        count = data.get('count', 1) if data else 1
        
        if count <= 0 or count > 100:
            return jsonify({'status': 'error', 'message': '生成数量必须在1-100之间'}), 400
        
        generated_cdks = []
        
        for _ in range(count):
            # 生成唯一的CDK码
            while True:
                cdk_code = generate_cdk_code()
                existing = CDK.query.filter_by(cdk_code=cdk_code).first()
                if not existing:
                    break
            
            # 创建新的CDK记录
            new_cdk = CDK(cdk_code=cdk_code)
            db.session.add(new_cdk)
            generated_cdks.append(cdk_code)
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': f'成功生成{count}个CDK',
            'cdks': generated_cdks
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': f'服务器错误: {str(e)}'}), 500

@cdk_bp.route('/list_cdks', methods=['GET'])
def list_cdks():
    """列出所有CDK（管理员功能）"""
    try:
        cdks = CDK.query.order_by(CDK.created_at.desc()).all()
        return jsonify({
            'status': 'success',
            'cdks': [cdk.to_dict() for cdk in cdks]
        }), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'服务器错误: {str(e)}'}), 500

@cdk_bp.route('/check_device', methods=['POST'])
def check_device():
    """检查设备授权状态"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': '请求数据格式错误'}), 400
        
        device_id = data.get('device_id', '').strip()
        
        if not device_id:
            return jsonify({'status': 'error', 'message': '设备ID不能为空'}), 400
        
        is_authorized = CDK.is_device_authorized(device_id)
        
        return jsonify({
            'status': 'success',
            'authorized': is_authorized,
            'message': '设备已授权' if is_authorized else '设备未授权'
        }), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'服务器错误: {str(e)}'}), 500

