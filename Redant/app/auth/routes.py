from flask import jsonify, request
from flask_jwt_extended import create_access_token
from flask import  Blueprint
from app.models import User
from app.extensions import db

# 数据验证模型

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住密码')
    submit = SubmitField('提交')


bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['POST'])
def login():
    # 尝试解析 JSON 数据
    json_data = request.get_json(silent=True)

    # 如果是 JSON 请求
    if json_data:
        login_name = json_data.get('login_name')
        login_pwd = json_data.get('login_pwd')
        print(login_name, login_pwd)
        if not all([login_name, login_pwd]):
            return jsonify({'code': 400, 'msg': '用户名和密码不能为空'}), 400
        return _handle_login(login_name, login_pwd)

    # 如果是表单提交（HTML）
    form = LoginForm()
    if form.validate_on_submit():
        return _handle_login(form.username.data, form.password.data)

    # 表单验证失败
    errors = {field.name: field.errors for field in form if field.errors}
    return jsonify({'code': 400, 'msg': '表单验证失败', 'errors': errors}), 400

def _handle_login(username, password):
    """统一的登录逻辑处理"""
    try:
        user = User.query.filter_by(login_name=username, login_pwd=password).first()
        if user:
            access_token = create_access_token(identity=user.uid)
            return jsonify({
                'code': 200,
                'msg': '登录成功',
                'token': access_token,
                'user_info': {'uid': user.uid, 'mobile': user.mobile}
            })
        return jsonify({'code': 401, 'msg': '用户名或密码错误'}), 401
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'msg': '服务器内部错误'}), 500
