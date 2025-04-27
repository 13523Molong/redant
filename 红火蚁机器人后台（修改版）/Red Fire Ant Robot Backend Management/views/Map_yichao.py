 
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
class Map_yichaoHandlers(RequestHandler):
    def initialize(self):
        # 这是一个变量，来记录是否重定向
        self.redir = False

        # 修改全局变量
        config.options['url'] = self.request.path
        # 查询缓存
        flag = self.application.inter.mymain(self.request.path, self)
        print("flag:",flag)
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
         # 处理HTTP GET请求
        resp_data = {}
        if h == "api_yichao_app":
            yichao_list = self.application.db.get_all_obj("select * from yichao","yichao")
            def convert_to_json_compatible(value):
                if isinstance(value, Decimal):
                    return float(value)
                elif isinstance(value, datetime):
                    return value.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    return value

            if len(yichao_list)==1:
                for k,v in yichao_list:
                    yichao_list[k] = convert_to_json_compatible(v) 
            elif len(yichao_list) > 1:
                for i in range(len(yichao_list)):
                    yichao = yichao_list[i]
                    keys_list = ['id', 'longitude', 'latitude', 'image', 'date', 'is_sanitized']  # 使用不同的变量名
                    for k in keys_list:
                        yichao[k] = convert_to_json_compatible(yichao[k])
                    yichao_list[i] = yichao

            # 更新原响应数据中的'data'部分
            resp_data['yichao'] = yichao_list #resp_data['yichao'] 是所有的蚁巢信息
            resp_data['current_user'] = config.options['current_user']  # 设置当前用户的信息
            json_str = json.dumps(resp_data, ensure_ascii=True)
            self.write(json_str)  
            return
        
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

       
        # 前端账户展示
        if h == "index":  
            # 如果h等于"index"
            resp_data = {}
            resp_data['status_mapping'] = config.STATUS_MAPPING
            resp_data['current_user'] = config.options['current_user']
            self.render("map_yichao/index2.html", resp_data=resp_data)
            # 渲染account/index.html模板并传入resp_data参数

        
        if h == "api_yichao":
            yichao_list = self.application.db.get_all_obj("select * from yichao","yichao")
            def convert_to_json_compatible(value):
                if isinstance(value, Decimal):
                    return float(value)
                elif isinstance(value, datetime):
                    return value.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    return value

            if len(yichao_list)==1:
                for k,v in yichao_list:
                    yichao_list[k] = convert_to_json_compatible(v) 
            elif len(yichao_list) > 1:
                for i in range(len(yichao_list)):
                    yichao = yichao_list[i]
                    keys_list = ['id', 'longitude', 'latitude', 'image', 'date', 'is_sanitized']  # 使用不同的变量名
                    for k in keys_list:
                        yichao[k] = convert_to_json_compatible(yichao[k])
                    yichao_list[i] = yichao

            # 更新原响应数据中的'data'部分
            resp_data['yichao'] = yichao_list #resp_data['yichao'] 是所有的蚁巢信息
            resp_data['current_user'] = config.options['current_user']  # 设置当前用户的信息
            json_str = json.dumps(resp_data, ensure_ascii=True)
            self.write(json_str)  
    