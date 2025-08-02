from extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    uid = db.Column(db.Integer, primary_key=True)
    login_name = db.Column(db.String(64), unique=True, nullable=False)
    login_pwd = db.Column(db.String(128), nullable=False)
    mobile = db.Column(db.String(11))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        # 返回一个格式化字符串，表示当前对象
        return f'<User {self.login_name}>'
