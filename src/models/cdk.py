from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class CDK(db.Model):
    __tablename__ = 'cdks'
    
    id = db.Column(db.Integer, primary_key=True)
    cdk_code = db.Column(db.String(32), unique=True, nullable=False)
    is_used = db.Column(db.Boolean, nullable=False, default=False)
    device_id = db.Column(db.String(128), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    used_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<CDK {self.cdk_code}>'

    def to_dict(self):
        return {
            'id': self.id,
            'cdk_code': self.cdk_code,
            'is_used': self.is_used,
            'device_id': self.device_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'used_at': self.used_at.isoformat() if self.used_at else None
        }

    def use_cdk(self, device_id):
        """使用CDK并绑定设备"""
        self.is_used = True
        self.device_id = device_id
        self.used_at = datetime.utcnow()
        db.session.commit()

    @staticmethod
    def verify_cdk(cdk_code, device_id):
        """验证CDK是否有效"""
        cdk = CDK.query.filter_by(cdk_code=cdk_code).first()
        
        if not cdk:
            return False, "CDK不存在"
        
        if cdk.is_used:
            if cdk.device_id == device_id:
                return True, "CDK已绑定当前设备"
            else:
                return False, "CDK已被其他设备使用"
        
        # CDK未使用，绑定到当前设备
        cdk.use_cdk(device_id)
        return True, "CDK验证成功，设备已绑定"

    @staticmethod
    def is_device_authorized(device_id):
        """检查设备是否已授权"""
        cdk = CDK.query.filter_by(device_id=device_id, is_used=True).first()
        return cdk is not None

