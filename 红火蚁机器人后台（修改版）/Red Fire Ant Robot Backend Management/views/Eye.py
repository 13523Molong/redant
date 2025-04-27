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
class EyeHandlers(RequestHandler):
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
        # 箱体中智能模块的窗口
        if h == "index":
            resp_data = {}
            # 从数据库中查询数据
            sql = "select * from bind"
            box_bind_data = self.application.db.get_all_obj(sql,"bind")
            print(box_bind_data)
            resp_data['box_bind_data'] = box_bind_data
            
            resp_data['current_user'] = config.options['current_user']
            self.render("eye/index.html", resp_data=resp_data)

        # 移动设备进入绑定窗口
        if h == "bind":
            resp_data = {}
            # 获取get参数
            module_name = self.get_argument("name",default="")
            module_id = self.get_argument("id",default="")
            resp_data['module'] = {}
            resp_data['module']['module_id'] = module_id
            resp_data['module']['module_name'] = config.MODULE_SELECT[int(module_name)-1]
            
            print(resp_data['module'])
            resp_data['current_user'] = config.options['current_user']
            resp_data['boxes'] = config.STATUS_BOXES
            self.render("eye/bind.html", resp_data=resp_data)
    
    def post(self,h):
        
        # 设备绑定以及相应的数据库操作
        if h == "bind":
            resp = {
                'code': 200,
                'msg': '设备绑定成功',
                'data': {}
            }
            # 获取数据
            id = self.get_body_argument("id",default="")
            name = self.get_body_argument("name",default="")
            box = self.get_body_argument("box",default="")
            # 数据库存储操作
            box_info = self.application.db.get_one("select * from bind where box_name='%s'" % box)
            if not box_info:
                resp['code'] = -1
                resp['msg'] = "操作失败"
                self.write(resp)
            status = "1"
            
            print(type(id))
            
            # 修改参数
            if name == "土壤模块":
                self.application.db.update("UPDATE bind SET soil_id='%s',soil_status='%s' where box_name='%s'" % (id,status, box))
            elif name == "温湿度模块":
                self.application.db.update("UPDATE bind SET T_H_id='%s',T_H_status='%s' where box_name='%s'" % (id,status, box))
            elif name=="水肥一体化模块":
                self.application.db.update("UPDATE bind SET fertilizer_id='%s',fertilizer_status='%s' where box_name='%s'" % (id,status, box))
            elif name=="灯板模块":
                self.application.db.update("UPDATE bind SET light_id='%s',light_status='%s' where box_name='%s'" % (id,status, box))
            else:
                resp['code'] = -1
                resp['msg'] = "数据库存储失败"
                self.write(resp)
            
            print(resp['msg'])
            resp['data'] = {'box':box}
            self.write(resp)
            
        # 按钮绑定的动态设置
        if h == "ops":
            resp = {
                'code':200,
                'msg':'操作成功',
                'data':{}
            }
            # 参数获取
            action = self.get_body_argument("act",default="")
            box_id = self.get_body_argument("id",default="")
            module_id = self.get_body_argument("module_id",default="")
            module_name = self.get_body_argument("module_name",default="")
            
            status = 1
            if action == "remove":
                status = 0
            elif action == "recover":
                status = 1
            else:
                status = None
            
            select_key = ""
            select_status = ""
            if module_name == "土壤模块":
                select_key = "soil_id"
                select_status = "soil_status"
                
            elif module_name == "温湿度模块":
                select_key = "T_H_id"
                select_status = "T_H_status"
                
            elif module_name == "水肥一体化模块":
                select_key = "fertilizer_id"
                select_status = "fertilizer_status"
                
            elif module_name == "光控模块":
                select_key = "light_id"
                select_status = "light_status"
                
            else:
                resp['code'] = -1
                resp['msg'] = "系统出错，操作失败"
                self.write(resp)
            
            # 执行sql语句更改数据库中的数据状态
            sql = "UPDATE bind  SET %s='%s',%s='%s' where box_name='%s'" % (select_key,module_id,select_status,status,box_id)
            
            # try:
            self.application.db.update(sql)
            # except :
            #     print("数据库操作出错")
            #     resp['code'] = -1
            #     resp['msg'] = "数据库操作异常"
            #     raise 

            self.write(resp)

