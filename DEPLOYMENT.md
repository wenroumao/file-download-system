# GitHub部署指南

本指南详细说明如何将文件下载系统部署到各种GitHub集成的平台。

## 项目准备

### 1. 创建GitHub仓库

1. 登录GitHub账户
2. 点击"New repository"创建新仓库
3. 仓库名称建议：`file-download-system`
4. 设置为Public（方便部署）
5. 不要初始化README（我们已经有了）

### 2. 推送代码到GitHub

```bash
# 添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/file-download-system.git

# 推送代码
git branch -M main
git push -u origin main
```

## 部署选项

### 方案一：Render部署（推荐）

#### 优势
- ✅ 完整的全栈应用支持
- ✅ 内置数据库支持
- ✅ 文件存储功能
- ✅ 免费层可用
- ✅ 自动HTTPS
- ✅ 简单配置

#### 部署步骤

1. **注册Render账户**
   - 访问 [render.com](https://render.com)
   - 使用GitHub账户登录

2. **连接GitHub**
   - 在Render Dashboard中点击"New +"
   - 选择"Web Service"
   - 连接GitHub账户
   - 选择您的仓库

3. **配置服务**
   ```
   Name: file-download-system
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python src/main.py
   ```

4. **设置环境变量**
   ```
   FLASK_ENV=production
   SECRET_KEY=your-secret-key-here
   ```

5. **部署**
   - 点击"Create Web Service"
   - 等待构建和部署完成
   - 获取部署URL

#### 预期结果
- 主网站：`https://your-app-name.onrender.com`
- 管理界面：`https://your-app-name.onrender.com/admin`

### 方案二：Railway部署

#### 优势
- ✅ 现代化界面
- ✅ 一键部署
- ✅ 自动扩展
- ✅ 免费层可用

#### 部署步骤

1. **注册Railway账户**
   - 访问 [railway.app](https://railway.app)
   - 使用GitHub账户登录

2. **部署项目**
   - 点击"New Project"
   - 选择"Deploy from GitHub repo"
   - 选择您的仓库
   - Railway会自动检测Python项目

3. **配置环境变量**
   ```
   FLASK_ENV=production
   SECRET_KEY=your-secret-key-here
   ```

4. **获取部署URL**
   - 在项目设置中生成域名
   - 访问您的应用

### 方案三：Vercel部署（需要重构）

#### 限制
- ⚠️ 需要重构为serverless架构
- ⚠️ 需要外部数据库
- ⚠️ 文件存储限制

#### 重构要求
1. 将Flask路由转换为Vercel Functions
2. 使用外部数据库服务（如PlanetScale）
3. 使用外部文件存储（如AWS S3）

## 部署后配置

### 1. 生成初始CDK

部署完成后，您需要生成一些CDK用于测试：

```bash
# 如果有SSH访问权限
python generate_cdk.py generate 10

# 或者通过管理界面生成
访问 https://your-app-url/admin
```

### 2. 测试功能

1. **访问主页面**
   - 检查界面是否正常显示
   - 确认设备ID自动生成

2. **测试CDK验证**
   - 输入生成的CDK码
   - 验证设备绑定功能

3. **测试文件下载**
   - 验证成功后下载文件
   - 确认文件下载正常

4. **测试管理界面**
   - 访问 `/admin` 路径
   - 测试CDK生成功能
   - 查看统计信息

### 3. 安全配置

1. **设置强密钥**
   ```
   SECRET_KEY=生成一个强随机密钥
   ```

2. **环境变量**
   ```
   FLASK_ENV=production
   ```

3. **域名配置**（可选）
   - 在部署平台中配置自定义域名
   - 设置DNS记录

## 监控和维护

### 1. 日志监控
- 在部署平台查看应用日志
- 监控错误和异常

### 2. 数据备份
- 定期备份SQLite数据库
- 备份重要的CDK数据

### 3. 性能监控
- 监控响应时间
- 检查资源使用情况

### 4. 更新部署
- 推送新代码到GitHub
- 平台会自动重新部署

## 故障排除

### 常见问题

1. **应用无法启动**
   - 检查requirements.txt是否完整
   - 确认Python版本兼容性
   - 查看构建日志

2. **数据库错误**
   - 确认数据库目录权限
   - 检查SQLite文件路径

3. **静态文件404**
   - 确认static目录存在
   - 检查文件路径配置

4. **API调用失败**
   - 检查CORS配置
   - 确认API路由正确

### 调试步骤

1. **查看日志**
   ```bash
   # 在部署平台查看应用日志
   ```

2. **测试本地运行**
   ```bash
   python src/main.py
   ```

3. **检查环境变量**
   ```bash
   # 确认所有必需的环境变量已设置
   ```

## 成本估算

### Render免费层
- 750小时/月运行时间
- 512MB RAM
- 适合小型项目

### Railway免费层
- $5免费额度/月
- 512MB RAM
- 1GB磁盘空间

### 升级建议
- 根据使用量选择付费计划
- 监控资源使用情况
- 考虑数据库备份服务

## 总结

推荐使用**Render**进行部署，因为：
1. 配置最简单
2. 完整功能支持
3. 免费层充足
4. 维护成本低

部署完成后，您将拥有一个完全功能的文件下载系统，支持CDK验证、设备绑定和安全文件下载。

