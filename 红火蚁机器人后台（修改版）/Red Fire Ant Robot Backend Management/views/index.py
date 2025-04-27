import tornado.web
from tornado.web import RequestHandler
from UserService import UserService
import config
import json
# 引入统一拦截器
from interceptor import Interceptor

import requests, time
from tornado.httpclient import AsyncHTTPClient
from tornado import gen

# 视图函数

# login_info = {
#             "login_pwd": "123456",
#             "login_name": "root",
#             "uid": 5,
#             "login_salt": "Q0kuBdTHrDAR1W1S"
#         }


class LoginHandlers(RequestHandler):
    # 登录功能
    def get(self):
        # 清理缓存,实现退出功能
        # print(self.get_cookie(name=config.cookies_name['name'], default='test'))
        # print(config.cookies_name['name'])
        self.clear_all_cookies()
        print("***********************")
        print(self.get_cookie(name=config.cookies_name['name'], default='test'))

        self.render("login.html")

    def post(self):
        resp = {
            'code': 200,
            'msg': "操作成功",
            'data': {}
        }
        # 获取用户的登录名称和登陆密码
        data = json.loads(self.request.body)
        login_name = data['login_name']
        login_pwd = data['login_pwd']
        print(login_pwd)
        print(login_name)
        # 进行参数有效性的校验h't
        if login_name is None or len(login_name) < 1:
            resp['code'] = -1
            resp['msg'] = "请输入符合规范的用户名"
            self.write(resp)

        if not login_pwd or len(login_pwd) < 1:
            resp['code'] = -1
            resp['msg'] = "请输入密码"
            self.write(resp)

        # 根据登录名称查询数据库中
        sql = "select * from user where login_name='{0}'".format(login_name)
        login_info = self.application.db.get_all_obj(sql, "user")


        if len(login_info) < 1:
            resp['code'] = -1
            resp['msg'] = "您的身份无权限"
            self.finish(resp)

        print("login_info=", login_info)
        login_info = login_info[0]
        if login_info['login_pwd'] != UserService.genePwd(login_pwd, login_info['login_salt']):
            resp['code'] = -1
            resp['msg'] = "登陆密码错误"
            self.finish(resp)

            # 设置cookies值
        self.set_cookie(config.cookies_name['name'], "%s#%s" % (UserService.geneAuthCode(login_info), login_info['uid']))
            # # # 数据库中查询用户信息并进行参数有效性的校验
        resp['cookie_key']=config.cookies_name['name']
        resp['cookie_value']="%s#%s" % (UserService.geneAuthCode(login_info), login_info['uid'])
        json_str = json.dumps(resp, ensure_ascii=True)
        self.write(json_str)


class IndexHandlers(RequestHandler):
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
        # 实现异步操作的测试
        # self.command()
        # self.test2()
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

            # 获取传感器的信息
            project_id = "0edf44222a80f31d2f60c015ff218024"
            device_id = "62ecc0ce3a88483559871f7e_box_01"
            server_id = "plants_box"
            info_url = "https://iotda.cn-north-4.myhuaweicloud.com/v5/iot/0edf44222a80f31d2f60c015ff218024/devices/62ecc0ce3a88483559871f7e_box_01/shadow"
            headers = {
                "User-Agent": "API Explorer",
                'X-Auth-Token': config.options['token'],
                'Content-Type': 'application/json;charset=UTF-8'
            }

            info = requests.get(url=info_url, headers=headers).json()
            # print("&&&&&")
            print(info['shadow'][1]['reported']['properties'])
            data = info['shadow'][1]['reported']['properties']

            # 数据展示
            f_heat = data['MT']
            f_wet = data['MH']
            e_heat = data['AT']
            e_wet = data['AH']
            PH = data['PH']
            CO2 = data['CO2']
            floor_N = data['N']
            floor_P = data['P']
            floor_K = data['K']
            # 电导率
            S = data['S']

            resp_data['environment'] = {
                'f_heat': f_heat,
                'f_wet': f_wet,
                'e_heat': e_heat,
                'e_wet': e_wet,
                'PH': PH,
                'floor_N': floor_N,
                'floor_P': floor_P,
                'floor_K': floor_K,
                'S': S,
                'CO2':CO2
            }

            self.render("index4.html", resp_data=resp_data)

        

    def post(self):
        resp = {
            'code': 200,
            'msg': '操作成功',
            'data': {}
        }
        self.write(resp)



    # 异步代码测试
    @gen.coroutine
    def command(self):
        client = AsyncHTTPClient()
        res = yield client.fetch("http://172.30.235.74:8008/hardware")
        if res.error:
            ret = {"ret": 0}
        else:
            ret = "successfully"
        raise tornado.gen.Return(ret)


    def test2(self):
        print("我是第二个函数")
        time.sleep(2)
        print("我走了")
