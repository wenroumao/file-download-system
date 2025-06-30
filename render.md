# Render.com deployment configuration

# Build Command (在Render中设置):
# pip install -r requirements.txt

# Start Command (在Render中设置):
# python src/main.py

# Environment Variables (在Render中设置):
# FLASK_ENV=production
# SECRET_KEY=your-secret-key-here
# PORT=10000

# 注意事项:
# 1. Render会自动设置PORT环境变量
# 2. 应用会自动使用环境变量中的PORT
# 3. 数据库文件会保存在持久化存储中
# 4. 静态文件已包含在项目中，无需单独构建

