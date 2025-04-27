import tornado.web
from tornado.web import RequestHandler
from UserService import UserService
import config


import tornado.web
from tornado.web import RequestHandler
from UserService import UserService
import config
# 引入统一拦截器
from interceptor import Interceptor

import requests, time
from tornado.httpclient import AsyncHTTPClient
from tornado import gen

class CommandHandlers(RequestHandler):
    def initialize(self):

        self.redir = False

        # 修改全局变量
        config.options['url'] = self.request.path
        # 查询缓存
        flag = self.application.inter.mymain(self.request.path, self)
        print(flag)
        if not flag:
            # self.redirect(config.domain_url['url'])
            self.redir = True

        else:
            self.redir = False
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
        # 教师命令的下发
        if h == "index":
            resp_data = {}
            resp_data['current_user'] = config.options['current_user']
            # 从数据库中将所有的数据查出来
            sql = "select * from wait_command where status=1"
            command_info = self.application.db.get_all_obj(sql, "wait_command")
            resp_data['list'] = command_info

            self.render("command/index.html", resp_data=resp_data, task=config.type_select)

        if h == "info":
            resp = {
                'code': 200,
                'msg': "操作成功",
                'data':{}
            }
            resp_data = {}
            resp_data['current_user'] = config.options['current_user']
            id = self.get_query_argument("id", default='')
            if not id:
                resp['code'] = -1
                resp['msg'] = "该任务不存在"
                self.write(resp)
            sql = "select * from wait_command where id='%s'" % (id)
            info = self.application.db.get_all_obj(sql, "wait_command")
            print(info)
            resp_data['info'] = info[0]

            self.render("command/info.html", resp_data=resp_data, task=config.type_select)

        if h == "finish":
            resp_data = {}
            resp_data['current_user'] = config.options['current_user']
            # 从数据库中查询已经失效的任务
            sql = "select * from wait_command where status=1"
            command_info = self.application.db.get_all_obj(sql, "wait_command")
            resp_data['list'] = command_info

            self.render("command/finish.html", resp_data=resp_data, task=config.type_select)

        if h == "add":
            resp_data = {}
            type_list = config.type_select
            resp_data['list'] = type_list
            resp_data['current_user'] = config.options['current_user']
            self.render("command/add.html", resp_data=resp_data, info=None, list=None)
        return


    def post(self, h):

        if h == "add":
            resp = {
                'code': 200,
                'msg': '命令发布成功',
                'data': {}
            }
            id = self.get_body_argument("id", default='')
            time = self.get_body_argument("time", default='')
            radius = self.get_body_argument("radius", default='')
            angle = self.get_body_argument("angle", default='')
            height = self.get_body_argument("height", default='')
            type = self.get_body_argument("type", default='')
            # 次数
            times = self.get_body_argument("times", default='')
            speed = self.get_body_argument("speed", default='')
            obj_id = self.get_body_argument("obj_id", default='')

            print("%%%%%%%%%%")
            #print(time)
            print("%%%%%%%%%%")

            # 进行参数有效性的校验
            if id is None or len(id) < 1:
                resp['code'] = -1
                resp['msg'] = "请输入符合的id"
                self.write(resp)

            if obj_id is None or len(obj_id) < 1:
                resp['code'] = -1
                resp['msg'] = "请输入环境终端集群号"
                self.write(resp)

            if time is None or time == "请选择日期 请选择时间":
                resp['code'] = -1
                resp['msg'] = "请输入时间"
                self.write(resp)

            timeArr = time.split(" ")
            if timeArr[0] == "请选择日期" or timeArr[1] == "请选择时间":
                resp['code'] = -1
                resp['msg'] = "请输入符合规范的时间"
                self.write(resp)


            if radius is None or len(radius) < 1:
                resp['code'] = -1
                resp['msg'] = "请输入符合规范发运行半径"
                self.write(resp)
            if angle is None or len(angle) < 1:
                resp['code'] = -1
                resp['msg'] = "请输入符合规范的俯仰角"
                self.write(resp)
            if height is None or len(height) < 1:
                resp['code'] = -1
                resp['msg'] = "请输入符合规范的运行高度"
                self.write(resp)
            if type is None or len(type) < 1:
                resp['code'] = -1
                resp['msg'] = "未设定任务类型"
                self.write(resp)
            if times is None or len(times) < 1:
                resp['code'] = -1
                resp['msg'] = "未设定次数"
                self.write(resp)
            if speed is None or len(speed) < 1:
                resp['code'] = -1
                resp['msg'] = "未设定速度"
                self.write(resp)

            cookies = self.get_cookie(config.cookies_name['name']).split("#")[1]

            member_info = self.application.db.get_one("select * from user where uid='%s'" % (int(cookies)))
            nickname = member_info[1]
            print(nickname)
        #     数据库存储
            has_in = self.application.db.get_one("select * from wait_command where id='%s'" % (id))
            if has_in:
                resp['code'] = -1
                resp['msg'] = "该任务已经存在"
                self.write(resp)

            # # 数据库添加
            self.application.db.insert("insert into wait_command (id,nickname,radius,height,speed,times,type,angle,start_time,obj_id) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (id, nickname, radius, height, speed, times, type, angle, time,obj_id))


            self.write(resp)


