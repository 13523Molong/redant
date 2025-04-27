# 路由映射子表
import tornado.web
import config
from views import index
from views import account
from views import User, Command, Stat, Eye,charts,Map,Map_yichao,Map_relitu,give_point
# give_point_one

# 引入数据库
from usrSQL import usrSQL
from interceptor import Interceptor

class Application(tornado.web.Application):
    def __init__(self):
        # 映射路由表
        handlers = [

            # 登录入口
            (r'/login', index.LoginHandlers),
            # 后台首页
            (r'/', index.IndexHandlers),
            # 分页路由
            (r'/map/(\w+)', Map.MapHandlers),
            (r'/map_yichao/(\w+)', Map_yichao.Map_yichaoHandlers),
            (r'/map_relitu/(\w+)', Map_relitu.Map_relituHandlers),
            (r'/charts', charts.ChartsHandlers),
            (r'/account/(\w+)', account.AccountHandlers),
            (r'/user/(\w+)', User.UserHandlers),
            (r'/command/(\w+)', Command.CommandHandlers),
            (r'/stat/(\w+)', Stat.StatHandlers),
            (r'/eye/(\w+)', Eye.EyeHandlers),
            (r'/give_point/(\w+)', give_point.give_pointHandlers),
            # (r'/give_point_one/(\w+)', give_point_one.give_point_oneHandlers),
           

        ]

        super(Application, self).__init__(handlers, **config.settings)
        self.db = usrSQL(config.mysql["host"], config.mysql["user"], config.mysql["password"], config.mysql["database"])
        self.inter = Interceptor(config.options['url'])




