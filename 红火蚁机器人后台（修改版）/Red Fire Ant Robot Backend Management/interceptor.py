
# 由于没有相应的统一拦截器的例子，所以只能自己写一个统一拦截器
import tornado.web as web
from tornado.web import RequestHandler
from UserService import UserService
import config
import re

class Interceptor():

    def __init__(self, path):
        self.path = path


    def mymain(self, path, req):

        # 静态文件的过滤
        ignore_urls = config.IGNORE_URLS
        ignore_check_login_urls = config.IGNORE_CHECK_LOGIN_URLS

        # 定义一个flag来标记是否用户有缓存值来记录用户的登录状态
        flag = True

        # 如果是静态文件就不查询用户信息了
        pattern = re.compile('%s' % "|".join(ignore_check_login_urls))
        if pattern.match(path):
            return flag

        if "/api" in path:
            return flag


        auth_cookie = req.get_cookie(name=config.cookies_name['name'], default='test')

        print(auth_cookie)

        # 进行cookie验证
        if auth_cookie == 'test':
            # print(11111)
            flag = False
            return flag

        auth_info = auth_cookie.split("#")
        if len(auth_info) != 2:
            flag = False
            return flag

        try:
            #   数据库查询
            sql = "select * from user where uid='%s'" % (auth_info[1])
            u_info = req.application.db.get_one(sql)
            print(u_info)
        #     将元组转换成字典形式
            user_info = {
                "nickname": u_info[1],
                "uid": u_info[0],
                "mobile": u_info[2],
                "email": u_info[3],
                "login_name": u_info[6],
                "login_pwd": u_info[7],
                "login_salt": u_info[8],
                "status": u_info[9]
            }
            config.options['current_user'] = user_info

        except Exception:
            return False

        if user_info is None:
            flag = False

        if auth_info[0] != UserService.geneAuthCode(user_info):
            #print(99999999)
            flag = False

        # 已经在登录的账号被删除立即退出
        if user_info["status"] != 1:
            flag = False

        # if user_info:
        #     flag = False

        pattern = re.compile('%s' % "|".join(ignore_urls))
        if pattern.match(path):
            return

        if not user_info:
            flag = False

        return flag
