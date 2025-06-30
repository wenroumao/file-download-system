from flask import Blueprint, request, jsonify, render_template_string
from src.models.cdk import CDK, db
import secrets
import string
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

def generate_cdk_code():
    """生成随机CDK码"""
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(16))

# 简单的管理界面HTML模板
ADMIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CDK管理系统</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 30px;
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        .section {
            margin-bottom: 30px;
            padding: 20px;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
        }
        .section h2 {
            margin-top: 0;
            color: #555;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: 500;
        }
        input, button {
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
        }
        input {
            width: 200px;
        }
        button {
            background-color: #007bff;
            color: white;
            border: none;
            cursor: pointer;
            margin-right: 10px;
        }
        button:hover {
            background-color: #0056b3;
        }
        .danger {
            background-color: #dc3545;
        }
        .danger:hover {
            background-color: #c82333;
        }
        .success {
            background-color: #28a745;
        }
        .success:hover {
            background-color: #218838;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 6px;
            text-align: center;
        }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #007bff;
        }
        .stat-label {
            color: #666;
            margin-top: 5px;
        }
        .cdk-list {
            max-height: 400px;
            overflow-y: auto;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
        }
        .cdk-item {
            padding: 10px;
            border-bottom: 1px solid #f0f0f0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .cdk-item:last-child {
            border-bottom: none;
        }
        .cdk-code {
            font-family: monospace;
            font-weight: bold;
        }
        .status {
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
        }
        .status.unused {
            background-color: #d4edda;
            color: #155724;
        }
        .status.used {
            background-color: #f8d7da;
            color: #721c24;
        }
        .message {
            padding: 10px;
            border-radius: 4px;
            margin: 10px 0;
        }
        .message.success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .message.error {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>CDK管理系统</h1>
        
        <div class="stats" id="stats">
            <!-- 统计信息将通过JavaScript加载 -->
        </div>
        
        <div class="section">
            <h2>生成CDK</h2>
            <div class="form-group">
                <label for="count">生成数量:</label>
                <input type="number" id="count" min="1" max="100" value="1">
                <button onclick="generateCDKs()" class="success">生成CDK</button>
            </div>
            <div id="generateMessage"></div>
        </div>
        
        <div class="section">
            <h2>CDK列表</h2>
            <button onclick="loadCDKs()">刷新列表</button>
            <button onclick="exportCDKs()" class="success">导出未使用CDK</button>
            <button onclick="deleteUsedCDKs()" class="danger">删除已使用CDK</button>
            <div id="cdkList" class="cdk-list">
                <!-- CDK列表将通过JavaScript加载 -->
            </div>
        </div>
    </div>

    <script>
        // 加载统计信息
        async function loadStats() {
            try {
                const response = await fetch('/admin/api/stats');
                const data = await response.json();
                
                document.getElementById('stats').innerHTML = `
                    <div class="stat-card">
                        <div class="stat-number">${data.total}</div>
                        <div class="stat-label">总CDK数</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${data.unused}</div>
                        <div class="stat-label">未使用</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${data.used}</div>
                        <div class="stat-label">已使用</div>
                    </div>
                `;
            } catch (error) {
                console.error('加载统计信息失败:', error);
            }
        }
        
        // 生成CDK
        async function generateCDKs() {
            const count = document.getElementById('count').value;
            const messageDiv = document.getElementById('generateMessage');
            
            if (!count || count < 1 || count > 100) {
                messageDiv.innerHTML = '<div class="message error">请输入1-100之间的数量</div>';
                return;
            }
            
            try {
                const response = await fetch('/api/generate_cdk', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ count: parseInt(count) })
                });
                
                const data = await response.json();
                
                if (data.status === 'success') {
                    messageDiv.innerHTML = `<div class="message success">成功生成 ${count} 个CDK</div>`;
                    loadStats();
                    loadCDKs();
                } else {
                    messageDiv.innerHTML = `<div class="message error">${data.message}</div>`;
                }
            } catch (error) {
                messageDiv.innerHTML = '<div class="message error">生成CDK失败</div>';
            }
        }
        
        // 加载CDK列表
        async function loadCDKs() {
            try {
                const response = await fetch('/api/list_cdks');
                const data = await response.json();
                
                const listDiv = document.getElementById('cdkList');
                
                if (data.status === 'success' && data.cdks.length > 0) {
                    listDiv.innerHTML = data.cdks.map(cdk => `
                        <div class="cdk-item">
                            <span class="cdk-code">${cdk.cdk_code}</span>
                            <span class="status ${cdk.is_used ? 'used' : 'unused'}">
                                ${cdk.is_used ? '已使用' : '未使用'}
                            </span>
                        </div>
                    `).join('');
                } else {
                    listDiv.innerHTML = '<div style="padding: 20px; text-align: center; color: #666;">暂无CDK记录</div>';
                }
            } catch (error) {
                console.error('加载CDK列表失败:', error);
            }
        }
        
        // 导出CDK
        async function exportCDKs() {
            try {
                const response = await fetch('/admin/api/export');
                const blob = await response.blob();
                
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `cdks_${new Date().toISOString().split('T')[0]}.txt`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
            } catch (error) {
                alert('导出失败');
            }
        }
        
        // 删除已使用的CDK
        async function deleteUsedCDKs() {
            if (!confirm('确定要删除所有已使用的CDK吗？此操作不可撤销！')) {
                return;
            }
            
            try {
                const response = await fetch('/admin/api/cleanup', {
                    method: 'DELETE'
                });
                const data = await response.json();
                
                if (data.status === 'success') {
                    alert(data.message);
                    loadStats();
                    loadCDKs();
                } else {
                    alert(data.message);
                }
            } catch (error) {
                alert('删除失败');
            }
        }
        
        // 页面加载时初始化
        window.onload = function() {
            loadStats();
            loadCDKs();
        };
    </script>
</body>
</html>
"""

@admin_bp.route('/')
def admin_dashboard():
    """管理员仪表板"""
    return render_template_string(ADMIN_TEMPLATE)

@admin_bp.route('/api/stats')
def get_stats():
    """获取CDK统计信息"""
    try:
        total = CDK.query.count()
        used = CDK.query.filter_by(is_used=True).count()
        unused = total - used
        
        return jsonify({
            'status': 'success',
            'total': total,
            'used': used,
            'unused': unused
        }), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'获取统计信息失败: {str(e)}'}), 500

@admin_bp.route('/api/export')
def export_cdks():
    """导出未使用的CDK"""
    try:
        cdks = CDK.query.filter_by(is_used=False).all()
        
        if not cdks:
            return jsonify({'status': 'error', 'message': '没有未使用的CDK可以导出'}), 404
        
        # 生成文本内容
        content = f"# CDK码列表\n"
        content += f"# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        content += f"# 总数量: {len(cdks)}\n\n"
        
        for cdk in cdks:
            content += f"{cdk.cdk_code}\n"
        
        from flask import Response
        return Response(
            content,
            mimetype='text/plain',
            headers={'Content-Disposition': f'attachment; filename=cdks_{datetime.now().strftime("%Y%m%d")}.txt'}
        )
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'导出失败: {str(e)}'}), 500

@admin_bp.route('/api/cleanup', methods=['DELETE'])
def cleanup_used_cdks():
    """删除已使用的CDK"""
    try:
        used_cdks = CDK.query.filter_by(is_used=True).all()
        
        if not used_cdks:
            return jsonify({'status': 'success', 'message': '没有已使用的CDK需要删除'}), 200
        
        count = len(used_cdks)
        
        for cdk in used_cdks:
            db.session.delete(cdk)
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': f'成功删除 {count} 个已使用的CDK'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': f'删除失败: {str(e)}'}), 500

