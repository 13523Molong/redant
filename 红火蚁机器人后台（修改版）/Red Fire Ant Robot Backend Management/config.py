import os
BASE_DIRS = os.path.dirname(__file__)

# 参数
options = {
    "port": 8009,
    "current_user": {},
    "token": "",
    "url": "http://172.30.255.74:8009"
   
}
# 数据库配置
mysql = {

    "host": "rm-wz9jcq0826443bm414o.mysql.rds.aliyuncs.com",
    "user": "root",
    "port": "3306",
    "password":"gz@84841383",
    "database": "honghuoyi"
}
STATUS_MAPPING = {
    "1": "正常",
    "0": "已删除"

}
# 分页
page = {
    'PAGE_SIZE': 10,
    'PAGE_DISPLAY': 10,

}

# 配置
settings = {
    "debug": True,
    "template_path": os.path.join(BASE_DIRS, "templates"),
    "static_path": os.path.join(BASE_DIRS, "static")
}

# 登录态cookies的名称
cookies_name = {
    'name': 'LOGIN'
}

# 统一拦截器配置
IGNORE_URLS = [
    "^/user/login",
    "^/api",
    "^/hardware",
    "^/eye",
   
]
IGNORE_CHECK_LOGIN_URLS = [
    "^/static",
    "^/favicon.ico"
]
# 172.30.255.74 本机ipv4
domain_url = {
    'url': "http://172.30.255.74:8009/login",
    'top_url': "http://172.30.255.74:8009",
    'cookie_domain': "172.30.255.74"
}

AK = 'CVFSH2COP4WCXM6ZFFUR',
SK = 'FZYIudRYYJCrtYnUojtYoGPwQihtdPu23puHQB0T',

# OBS = {
#     'bucketName': 'smart-plants-box',
#     'objectKey': 'videos',
#     'downPath': 'http://192.168.2.21:5653/static/download',
# }

# 运动方式
type_select = [{'id': 1, 'name': '中部环绕采样'}, {'id': 2, 'name': '顶部环绕采样'}]
# 光谱波段
light_type_select = [
                        {'id': 1, 'name': '200'},
                        {'id': 2, 'name': '380'},
                        {'id': 3, 'name': '400'},
                        {'id': 4, 'name': '420'},
                        {'id': 5, 'name': '440'},
                        {'id': 6, 'name': '460'},
                        {'id': 7, 'name': '480'},
                        {'id': 8, 'name': '500'},
                        {'id': 9, 'name': '520'},
                        {'id': 10, 'name': '540'},
                        {'id': 11, 'name': '560'},
                        {'id': 12, 'name': '580'},
                        {'id': 13, 'name': '600'},
                        {'id': 14, 'name': '620'},
                        {'id': 15, 'name': '640'},
                        {'id': 16, 'name': '660'},
                        {'id': 17, 'name': '680'},
                        {'id': 18, 'name': '700'},
                        {'id': 19, 'name': '720'},
                        {'id': 20, 'name': '740'},
                        {'id': 21, 'name': '760'},
                        {'id': 22, 'name': '780'},
                        {'id': 23, 'name': '800'},
                    ]
#培育箱
STATUS_BOXES = [{'id':1,'name':'环境集群1号'},{'id':2,'name':'环境集群2号'}]
# 可供选择的智能模块的名称
STATUS_MODULE = [{'module_id':1,'name':'水肥模块'},{'module_id':2,'name':'温湿模块'},{'module_id':3,'name':'水肥模块'},{'module_id':4,'name':'灯控模块'}]
MODULE_SELECT = ['碳氧模块','温湿模块','水肥模块','灯控模块']

# 判断智能模块是否已经绑定
BIND_IF = ['已绑定','未绑定']
