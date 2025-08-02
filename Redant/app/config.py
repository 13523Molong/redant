import os
from datetime import timedelta

class Config:
    # 基础配置
    SECRET_KEY = 'Mmyshi@13579'
    
    # JWT配置
    JWT_SECRET_KEY = "嘻嘻嘻嘻嘻嘻"  # 生产环境应使用环境变量
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
    
    # 数据库配置
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'Mmyshi13579'
    MYSQL_HOST = 'rm-bp1b3w6vp958h2rbvio.mysql.rds.aliyuncs.com'
    MYSQL_PORT = '3306'
    MYSQL_DB = 'redant'
    
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    REDIS_PASSWORD = '123456'
    
    # 应用程序配置
    ORIGIN_POINT = {
        'latitude': 28.174792,
        'longitude': 112.945643
    }
