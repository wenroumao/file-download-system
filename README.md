# 文件下载系统 - CDK验证

一个基于Flask和React的全栈文件下载系统，支持CDK验证、设备绑定和安全文件下载。

## 功能特性

### 用户功能
- 🔐 CDK验证和设备绑定
- 📱 设备唯一性识别
- 📥 安全文件下载
- 🎨 现代化用户界面

### 管理员功能
- 🎫 CDK批量生成
- 📊 使用统计查看
- 📋 CDK状态管理
- 📤 数据导出和清理
- 📁 文件上传管理

### 安全特性
- 🔒 一次性CDK使用机制
- 🔗 设备唯一性绑定
- 🛡️ 文件访问权限控制
- 🔐 安全的API接口

## 技术栈

### 后端
- **框架**: Flask (Python)
- **数据库**: SQLite + SQLAlchemy
- **跨域**: Flask-CORS
- **文件处理**: Python标准库

### 前端
- **框架**: React 18
- **UI库**: shadcn/ui
- **样式**: Tailwind CSS
- **图标**: Lucide React
- **构建工具**: Vite

## 快速开始

### 本地开发

1. **克隆项目**
```bash
git clone <repository-url>
cd file-download-system-github
```

2. **安装Python依赖**
```bash
pip install -r requirements.txt
```

3. **运行应用**
```bash
python src/main.py
```

4. **访问应用**
- 主网站: http://localhost:5001
- 管理界面: http://localhost:5001/admin

### CDK管理

使用命令行工具管理CDK：

```bash
# 生成CDK
python generate_cdk.py generate 10

# 查看CDK列表
python generate_cdk.py list

# 导出未使用CDK
python generate_cdk.py export cdks.txt

# 清理已使用CDK
python generate_cdk.py cleanup
```

## 部署

### Render部署

1. 连接GitHub账户到Render
2. 选择此仓库创建新服务
3. 使用以下配置：
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python src/main.py`
   - **Environment**: Python 3

### 环境变量

可选的环境变量配置：

- `FLASK_ENV`: 设置为 `production`
- `SECRET_KEY`: Flask密钥（生产环境建议设置）
- `PORT`: 端口号（默认5001）

## API文档

### 用户API

#### CDK验证
```
POST /api/verify_cdk
Content-Type: application/json

{
  "cdk": "CDK码",
  "device_id": "设备ID"
}
```

#### 文件下载
```
GET /api/download_file?device_id=设备ID
```

### 管理API

#### 获取统计信息
```
GET /admin/api/stats
```

#### 生成CDK
```
POST /admin/api/generate
Content-Type: application/json

{
  "count": 10
}
```

## 项目结构

```
file-download-system-github/
├── src/
│   ├── models/          # 数据模型
│   │   ├── user.py      # 用户模型
│   │   └── cdk.py       # CDK模型
│   ├── routes/          # API路由
│   │   ├── user.py      # 用户路由
│   │   ├── cdk.py       # CDK路由
│   │   └── admin.py     # 管理路由
│   ├── static/          # 前端静态文件
│   ├── files/           # 文件存储目录
│   ├── database/        # 数据库文件
│   └── main.py          # 主应用文件
├── generate_cdk.py      # CDK生成脚本
├── requirements.txt     # Python依赖
└── README.md           # 项目说明
```

## 安全说明

### CDK安全机制
- 16位随机生成的CDK码
- 一次性使用，使用后立即标记为已用
- 与设备ID绑定，防止跨设备使用

### 设备识别
- 基于浏览器信息生成唯一设备ID
- 包含用户代理、平台、语言、屏幕分辨率、时区等信息
- 生成稳定的哈希值作为设备标识

### 文件保护
- 文件存储在服务器受保护目录
- 只有通过API验证的设备才能下载
- 下载时验证设备授权状态

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request来改进项目。

## 支持

如有问题，请创建Issue或联系项目维护者。



## 文件上传功能

### 功能概述
管理员可以通过网页界面直接上传文件到服务器，无需手动操作服务器文件系统。

### 支持的文件类型
- **压缩文件**: zip, rar, 7z, tar, gz
- **可执行文件**: exe
- **文档文件**: pdf, doc, docx, txt

### 使用方法
1. 访问管理界面：`http://your-domain/admin`
2. 在"文件上传"区域点击"选择文件"
3. 选择要上传的文件（最大100MB）
4. 点击"上传文件"按钮
5. 等待上传完成，查看结果消息

### 安全限制
- **文件大小**: 最大100MB
- **文件类型**: 仅允许预定义的安全文件类型
- **访问权限**: 仅管理员可以上传文件
- **存储安全**: 文件名自动处理，防止路径遍历攻击

### 上传后的文件
- 文件保存在服务器的 `src/files/` 目录
- 用户可以通过CDK验证后下载这些文件
- 支持文件覆盖（同名文件会被替换）

