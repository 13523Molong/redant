# Flask 后端服文档

## 项目概述

这是一个基于Flask框架的完整后端服务解决方案，提供以下核心功能：
- ✅ 用户认证与JWT令牌管理
- 📍 地图坐标处理与存储
- 🚗 车辆导航路线计算
- 🗄️ 两种MySQL数据库连接方案
- 🌐 跨域请求支持

## 系统架构
···
Flask Application
├── API Endpoints
│ ├── Auth API (JWT)
│ ├── Map Points API
│ └── Navigation API
├── Database Layer
│ ├── Native MySQL Connector
│ └── SQLAlchemy ORM (可选)
└── Utilities
├── Connection Pooling
└── Result Formatters
···

## 详细技术说明

### 1. 核心配置

#### JWT配置
```python
app.config["JWT_SECRET_KEY"] = "your_super_secret_key_here"  # 生产环境应更复杂
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=2)
```
#### 数据库连接
```python
//返岗一:原生MySQL连接器(目前使用)
class MySQLDatabase:
    def __init__(self, config):
        self.config = config
        self.connection = None
    
    def __enter__(self):
        self.connection = mysql.connector.connect(**self.config)
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection and self.connection.is_connected():
            self.connection.close()


//方案二LSQLAlchemy ORM(开发中推荐)
app.config['SQLALCHEMY_DATABASE_URI'] = 
    f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
db = SQLAlchemy(app)
