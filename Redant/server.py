from flask import (
    Flask, 
    jsonify,
    request,
    redirect,
    url_for,
make_response)

import flask.sessions
#配置跨域，是不同浏览器兼容
from flask_cors import CORS

from config import *

from sqlalchemy import *

# from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import event

from sqlalchemy.exc import SQLAlchemyError, DisconnectionError

# 导入数据库配置信息
from database import *

from flask_sqlalchemy import *

from flask.views import MethodView

from sqlalchemy.exc import SQLAlchemyError

import numpy as np

import datetime

from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField, BooleanField

from wtforms.validators import DataRequired, Length, Email, EqualTo

# from db_connect_test import *
# 创建Flask实例



app = Flask(__name__)

# 配置JWT相关参数
app.config["JWT_SECRET_KEY"] = "your_super_secret_key_here"  # 生产环境用更复杂的密钥
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=2)  # Token有效期
jwt = JWTManager(app)

# 配置跨域   允许发送跨域请求，cookies支持


# Flask 配置跨域示例（确保安装了 flask_cors）
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

#配置会话密钥
app.secret_key = 'Mmyshi@13579'

#配置时间监听器，监听数据库连接是否丢失
# def handle_disconnection(dbapi_connection, connection_record):
#     if isinstance(dbapi_connection.proxy, DisconnectionError):
#         connection_record._connection = None

# # 注册事件监听器
# event.listen(mydb, 'handle_disconnect', handle_disconnection)



# 配置数据库连接信息
# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{mysql_user}:{mysql_pwd}@{mysql_host}:{mysql_port}/{mysql_db}'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# mydb.init_app(app)




#创建蓝图对象


#配置登录检验
class LoginForm(FlaskForm):
    username = StringField('用户名')
    password = PasswordField('密码')
    remember_me = BooleanField('记住密码')
    submit = SubmitField('提交')




class LoginApi(MethodView):
    def post(self):
        # 尝试解析 JSON 数据
        json_data = request.get_json(silent=True)
        
        # 如果是 JSON 请求
        if json_data:
            login_name = json_data.get('login_name')
            login_pwd = json_data.get('login_pwd')
            if not all([login_name, login_pwd]):
                return jsonify({'code': 400, 'msg': '用户名和密码不能为空'}), 400
            return self._handle_login(login_name, login_pwd)
        
        # 如果是表单提交（HTML）
        form = LoginForm()
        if form.validate_on_submit():
            return self._handle_login(form.username.data, form.password.data)
        
        # 表单验证失败
        errors = {field.name: field.errors for field in form if field.errors}
        return jsonify({'code': 400, 'msg': '表单验证失败', 'errors': errors}), 400

    def _handle_login(self, username, password):
        """统一的登录逻辑处理"""
        try:
            with MySQLConnect() as db:
                with db.cursor(dictionary=True) as cursor:
                    cursor.execute(
                        'SELECT uid, mobile FROM user WHERE login_name = %s AND login_pwd = %s',
                        (username, password)
                    )
                    user = cursor.fetchone()
                    if user:
                        access_token = create_access_token(identity=user['uid'])
                        return jsonify({
                            'code': 200,
                            'msg': '登录成功',
                            'token': access_token,
                            'user_info': {'uid': user['uid'], 'mobile': user['mobile']}
                        })
                    return jsonify({'code': 401, 'msg': '用户名或密码错误'}), 401
        except mysql.connector.Error as e:
            app.logger.error(f"数据库错误: {e}")
            return jsonify({'code': 500, 'msg': '服务器内部错误'}), 500


    def get(self):
        print('get')
        return jsonify({'msg': '成功访问,测试Sucess'})

app.add_url_rule('/index/',view_func=LoginApi.as_view('login'))   



#用于处理地图多端选点发送的经纬度数组，进行调整，使其与原点保持共线


class SendPointAPI(MethodView):
    def post(self):
       
        
        data = request.json
        points = data.get('points', [])
        origin = [28.174792, 112.945643]  # 原点坐标

        # 转换数据类型并保留两位小数
        points = [{'latitude': float(point['latitude']), 'longitude': float(point['longitude'])} for point in points]

        carID = data.get('carID')
        print("Received Points:", points)
        print("Car ID:", carID)

        # 调整坐标
        adjusted_points = self.adjust_coordinates(points, origin)
        self.insert_car_run_info(carID, adjusted_points)
        return jsonify({'adjustedPoints': adjusted_points})

    @staticmethod
    def adjust_coordinates(points, origin):
        if len(points) < 1:
            # 如果没有点，不进行调整
            return points

        # 计算纬度和经度的差异
        lat_diffs = [abs(point['latitude'] - origin[0]) for point in points]
        lng_diffs = [abs(point['longitude'] - origin[1]) for point in points]

        # 判断纬度差异和经度差异的最大值
        if max(lat_diffs) < max(lng_diffs):
            # 如果纬度差异较小，调整所有点的纬度为原点纬度
            adjusted_points = [{'latitude': origin[0], 'longitude': point['longitude']} for point in points]
        else:
            # 如果经度差异较小，调整所有点的经度为原点经度
            adjusted_points = [{'latitude': point['latitude'], 'longitude': origin[1]} for point in points]

        return adjusted_points
        
    # 自定义动态时间戳
    @staticmethod
    def create_time():
        """
            生成一个唯一的时间戳，精确到秒。
        """
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def insert_car_run_info(self, carID, points):
            created_time = self.create_time()  # 为每个点生成不同的时间戳
            query = """
            INSERT INTO give_point (carID, longitude, latitude, created_time)
            VALUES (%s, %s, %s, %s)
            """
            values = [(carID, point['longitude'], point['latitude'], created_time) for point in points]
            try:
                db = MySQLConnect()
                cursor = db.cursor(dictionary=True)
                # 检查mysql数据库是连接在线
                
                try:
                    if db.is_connected():
                        print("数据库已连接")
                        db.ping(reconnect=True)
                        print("正在尝试重新连接...")
                
                except mysql.connector.Error as err:
                    print("数据库连接失败: {}".format(err))
        
            
                cursor.executemany(query,values) 
                db.commit()
                print(f"成功插入记录到 give_point 表中。")
            except mysql.connector.Error as e:
                db.rollback()
                print(f"插入失败: {e}")
            finally:
                cursor.close()
                db.close()
                
                
# 路由绑定
app.add_url_rule('/send_point/', view_func=SendPointAPI.as_view('send_point'))



class NavigationAPI(MethodView):

    def post(self):
        data = request.json
        robot_position=data.get('robot_position')
        target_position=data.get('target_position')



        print(f"Start Point: {robot_position}, End Point: {target_position}")
        return jsonify({'message': 'Navigation route calculated successfully.'})
      
app.add_url_rule('/navigation/', view_func=NavigationAPI.as_view('navigation'))
             
class LMUsaveApi(MethodView):
    def post(self):
        data = request.json
        IMU2 = data.get('')
        IMU2 = data.get('')
        
        pass
        



class give_pointAPi(MethodView):
    def get(self):
        pass
    
        
        

if __name__ == '__main__':

        # 在应用上下文中执行代码
        app.run(debug=True, host='0.0.0.0', port=5003)

