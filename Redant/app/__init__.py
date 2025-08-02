from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
from extensions import db
from config import Config
import logging

def create_app(config_class=Config):
    # 配置日志
    logging.basicConfig(level=logging.INFO)
    
    app = Flask(__name__)
    app.logger.info('Starting Flask application...')
    
    # 加载配置
    app.config.from_object(config_class)
    app.logger.info('Configuration loaded')
    
    # 初始化扩展
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
    JWTManager(app)
    db.init_app(app)
    app.logger.info('Extensions initialized')
    
    # 注册蓝图
    from auth.routes import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from utils import bp as utils_bp
    app.register_blueprint(utils_bp, url_prefix='/index')
    
    # app.logger.info('All blueprints registered')
    # app.logger.info(f'Available routes: {[rule.rule for rule in app.url_map.iter_rules()]}')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5003)
