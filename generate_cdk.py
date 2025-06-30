#!/usr/bin/env python3
"""
CDK生成和管理脚本
用于生成CDK码和管理CDK数据库
"""

import os
import sys
import argparse
import secrets
import string
from datetime import datetime

# 添加项目路径
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask
from src.models.user import db
from src.models.cdk import CDK

def create_app():
    """创建Flask应用实例"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'src', 'database', 'app.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

def generate_cdk_code():
    """生成随机CDK码"""
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(16))

def generate_cdks(count):
    """生成指定数量的CDK"""
    app = create_app()
    
    with app.app_context():
        # 确保数据库表存在
        db.create_all()
        
        generated_cdks = []
        
        for i in range(count):
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
            
            print(f"生成CDK {i+1}/{count}: {cdk_code}")
        
        try:
            db.session.commit()
            print(f"\n成功生成 {count} 个CDK码！")
            return generated_cdks
        except Exception as e:
            db.session.rollback()
            print(f"生成CDK时发生错误: {e}")
            return []

def list_cdks():
    """列出所有CDK"""
    app = create_app()
    
    with app.app_context():
        cdks = CDK.query.order_by(CDK.created_at.desc()).all()
        
        if not cdks:
            print("数据库中没有CDK记录")
            return
        
        print(f"\n共找到 {len(cdks)} 个CDK:")
        print("-" * 80)
        print(f"{'CDK码':<20} {'状态':<10} {'设备ID':<20} {'创建时间':<20} {'使用时间':<20}")
        print("-" * 80)
        
        for cdk in cdks:
            status = "已使用" if cdk.is_used else "未使用"
            device_id = cdk.device_id[:16] + "..." if cdk.device_id and len(cdk.device_id) > 16 else (cdk.device_id or "")
            created_at = cdk.created_at.strftime("%Y-%m-%d %H:%M") if cdk.created_at else ""
            used_at = cdk.used_at.strftime("%Y-%m-%d %H:%M") if cdk.used_at else ""
            
            print(f"{cdk.cdk_code:<20} {status:<10} {device_id:<20} {created_at:<20} {used_at:<20}")

def export_cdks(filename):
    """导出CDK到文件"""
    app = create_app()
    
    with app.app_context():
        cdks = CDK.query.filter_by(is_used=False).all()
        
        if not cdks:
            print("没有未使用的CDK可以导出")
            return
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("# CDK码列表\n")
                f.write(f"# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# 总数量: {len(cdks)}\n\n")
                
                for cdk in cdks:
                    f.write(f"{cdk.cdk_code}\n")
            
            print(f"成功导出 {len(cdks)} 个未使用的CDK到文件: {filename}")
        except Exception as e:
            print(f"导出CDK时发生错误: {e}")

def delete_used_cdks():
    """删除已使用的CDK"""
    app = create_app()
    
    with app.app_context():
        used_cdks = CDK.query.filter_by(is_used=True).all()
        
        if not used_cdks:
            print("没有已使用的CDK需要删除")
            return
        
        count = len(used_cdks)
        confirm = input(f"确定要删除 {count} 个已使用的CDK吗？(y/N): ")
        
        if confirm.lower() == 'y':
            try:
                for cdk in used_cdks:
                    db.session.delete(cdk)
                db.session.commit()
                print(f"成功删除 {count} 个已使用的CDK")
            except Exception as e:
                db.session.rollback()
                print(f"删除CDK时发生错误: {e}")
        else:
            print("操作已取消")

def main():
    parser = argparse.ArgumentParser(description='CDK生成和管理工具')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 生成CDK命令
    generate_parser = subparsers.add_parser('generate', help='生成CDK')
    generate_parser.add_argument('count', type=int, help='要生成的CDK数量')
    
    # 列出CDK命令
    list_parser = subparsers.add_parser('list', help='列出所有CDK')
    
    # 导出CDK命令
    export_parser = subparsers.add_parser('export', help='导出未使用的CDK到文件')
    export_parser.add_argument('filename', help='导出文件名')
    
    # 删除已使用CDK命令
    delete_parser = subparsers.add_parser('cleanup', help='删除已使用的CDK')
    
    args = parser.parse_args()
    
    if args.command == 'generate':
        if args.count <= 0 or args.count > 1000:
            print("CDK数量必须在1-1000之间")
            return
        generate_cdks(args.count)
    elif args.command == 'list':
        list_cdks()
    elif args.command == 'export':
        export_cdks(args.filename)
    elif args.command == 'cleanup':
        delete_used_cdks()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()

