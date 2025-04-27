import tornado.web
from tornado.web import RequestHandler
from UserService import UserService
import config
import os
import tornado.ioloop
import tornado.escape
from views import test
import json

import tornado.web
from tornado.web import RequestHandler
from UserService import UserService
import config
# 引入统一拦截器
from interceptor import Interceptor

import requests, time
from tornado.httpclient import AsyncHTTPClient
from tornado import gen

class ChartsHandlers(RequestHandler):
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


    def get(self):
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
        resp_data = {}
        resp_data['current_user'] = config.options['current_user']
        self.render("charts.html", resp_data=resp_data)
    
       