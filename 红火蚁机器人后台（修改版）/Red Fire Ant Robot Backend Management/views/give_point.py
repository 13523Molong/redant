# -*- coding: utf-8 -*-
from decimal import Decimal
from tornado.web import RequestHandler
from Helper import iPagination
import config
import json
from datetime import datetime
import base64
import io
# from PIL import Image
import tornado.web
from tornado.web import RequestHandler
from UserService import UserService
import config
# 引入统一拦截器
from interceptor import Interceptor
import requests, time
from tornado.httpclient import AsyncHTTPClient
from tornado import gen
class give_pointHandlers(RequestHandler):
    def initialize(self):
        # 这是一个变量，来记录是否重定向
        self.redir = False

        # 修改全局变量
        config.options['url'] = self.request.path
        # 查询缓存
        flag = self.application.inter.mymain(self.request.path, self)
        print("index_flag:",flag)
        if not flag:
            # self.redirect(config.domain_url['url'])
            self.redir = True
        else:
            self.redir = False


        # 向华为云获取token值并储存在全局变量中

        url = 'https://iam.cn-north-4.myhuaweicloud.com/v3/auth/tokens'
        data = {
            "auth": {
                "identity": {
                    "methods": ["password"],
                    "password": {
                        "user": {
                            "name": "NikkoLKR",
                            "password": "lkr3931978",

                            "domain": {
                                "name": "NikkoLKR"
                            }
                        }
                    }
                },
                "scope": {
                    "project": {
                        "name": "cn-north-4"
                    }
                }
            }
        }
        headers = {'Content-Type': 'application/json;charset=UTF-8'}
        req = requests.post(url, json=data)
        token = req.headers['X-Subject-Token']
        # 将token值存储到全局变量中
        config.options['token'] = token

        return


    def get(self, h):  
        if self.redir == True:
            # print({"left********"})
            self.redirect(config.domain_url['url'])

        else:
            # 获取cookies来进行页面展示
            cookies = self.get_cookie(name=config.cookies_name['name'])
            uid = cookies.split("#")[1]
            # 数据库查询
            sql = "select * from user where uid='%s'" % (uid)
            u_info = self.application.db.get_one(sql)
            info = {
                "nickname": u_info[1],
                'mobile': u_info[2]
            }

            resp_data = {}
            resp_data['current_user'] = config.options['current_user']
        # 处理HTTP GET请求
        resp_data = {}
        if h == "index":  
            # 如果h等于"index"
            resp_data = {}
            resp_data['status_mapping'] = config.STATUS_MAPPING
            resp_data['current_user'] = config.options['current_user']
            self.render("give_point/index2.html", resp_data=resp_data)
            # 渲染account/index.html模板并传入resp_data参数

        # 添加账号操作
        # if h == "api_to_map":
        #     resp = {
        #         'code': 200,
        #         'msg': "操作成功",
        #         'data': {}
        #     }
        #     give_point_list = self.application.db.get_all_obj("select * from give_point", "give_point")
        #     resp["data"] = give_point_list
        #     self.write(json.dumps(resp))

        if h == "api_index":
            give_point_list = self.application.db.get_all_obj("select * from give_point","give_point")
            def convert_to_json_compatible(value):
                if isinstance(value, Decimal):
                    return float(value)
                elif isinstance(value, datetime):
                    return value.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    return value

            if len(give_point_list)==1:
                for k,v in give_point_list:
                    give_point_list[k] = convert_to_json_compatible(v) 
            elif len(give_point_list) > 1:
                for i in range(len(give_point_list)):
                    give_point = give_point_list[i]
                    keys_list = ['carid', 'longitude', 'latitude', 'created_time']  # 使用不同的变量名
                    for k in keys_list:
                        give_point[k] = convert_to_json_compatible(give_point[k])
                    give_point_list[i] = give_point

            # 更新原响应数据中的'data'部分
            resp_data['give_point'] = give_point_list #resp_data['yichao'] 是所有的蚁巢信息
            resp_data['current_user'] = config.options['current_user']  # 设置当前用户的信息
            json_str = json.dumps(resp_data, ensure_ascii=True)
            self.write(json_str)  
    def post(self, h):  # 处理HTTP POST请求
        # 添加账号操作
        if h == "api":
            resp = {
                'code': 200,
                'msg': "操作成功",
                'data': {}
            }
            carID = self.get_body_argument("carID", default="1")
            # 从请求体中提取参数
            all_path = self.get_body_argument("allPath", default="[]")
            try:
                # 解析 JSON 字符串
                all_path = json.loads(all_path)
            except json.JSONDecodeError:
                self.set_status(400)
                self.write({"code": 400, "msg": "Invalid JSON format for allPath"})
                return
            # try:
            #     body = json.loads(self.request.body)
            #     carID = body.get("carID", "1")
            #     allPath = body.get("allPath", "0")
            # except json.JSONDecodeError:
            #     resp['code'] = -1
            #     resp['msg'] = "无效的请求数据"
            #     self.write(json.dumps(resp))
            #     return

            give_point_list = self.application.db.get_all_obj("select * from give_point", "give_point")
            for i in range(0, len(all_path), 5):        
                longitude = all_path[i][0]
                latitude  = all_path[i][1]
                # 执行批量插入
                self.application.db.insert(
                    "INSERT INTO give_point (carID, longitude, latitude) VALUES (%s, %s, %s)" % (carID, longitude, latitude)
                )
            self.write(json.dumps(resp))
        if h == "api_app":
            resp = {
                'code': 200,
                'msg': "操作成功",
                'data': {}
            }
            try:
                body = json.loads(self.request.body)
                carID = body.get("carID", "1")
                longitude = body.get("longitude", 0)
                latitude = body.get("latitude", 0)
            except json.JSONDecodeError:
                resp['code'] = -1
                resp['msg'] = "无效的请求数据"
                self.write(json.dumps(resp))
                return

            if not carID:
                resp['code'] = -1
                resp['msg'] = "请输入小车编号"
                self.write(json.dumps(resp))
                return
            if not longitude:
                resp['code'] = -1
                resp['msg'] = "请输入经度"
                self.write(json.dumps(resp))
                return
            if not latitude:
                resp['code'] = -1
                resp['msg'] = "请输入纬度"
                self.write(json.dumps(resp))
                return

            give_point_list = self.application.db.get_all_obj("select * from give_point", "give_point")
            self.application.db.insert("INSERT INTO give_point (carID, longitude, latitude) VALUES (%s, %s, %s)" % (carID, longitude, latitude))
            self.write(json.dumps(resp))