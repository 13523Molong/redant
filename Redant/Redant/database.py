#数据库连接方式一
import mysql.connector 

from decimal import Decimal

import mysql.connector


#数据库管理模块
class MySQLDatabase:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        """建立数据库连接"""
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        return self.connection

    def close(self):
        """关闭数据库连接"""
        if self.connection and self.connection.is_connected():
            self.connection.close()



def MySQLConnect():
    mydb = mysql.connector.connect(
        host='rm-bp1b3w6vp958h2rbvio.mysql.rds.aliyuncs.com',  # IP或域名
        port=3306,  # 端口，默认3306
        user='root',  # 数据库用户名
        password='Mmyshi13579',  # 数据库登录密码
        database='redant',  # 要连接的数据库
    )
    return mydb


def showtables(myresult):
    for x in myresult:
        print(x)


def printResult(myresult):
    
    for x in myresult:
        data={
            'Carid':x[0],
            'longtitude':x[1],
            'latitude':x[2],
            'datatime':x[3],
        }
        for key, value in data.items():
            print(f"{key}: {value}")



#数据库连接方式二

# from flask_sqlalchemy import SQLAlchemy

# import pymysql 
    
# pymysql.install_as_MySQLdb()

# mydb = SQLAlchemy()



