from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # 导入CORS
from flask_migrate import Migrate  # 导入 Flask-Migrate
import os

db = SQLAlchemy()  # 初始化数据库
migrate = Migrate()  # 初始化 Flask-Migrate

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})  # 启用CORS

    # 获取当前文件（__init__.py）的绝对路径
    base_dir = os.path.abspath(os.path.dirname(__file__))

    # 配置数据库的绝对路径
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'game_assistant.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)  # 将数据库绑定到 Flask 应用
    migrate.init_app(app, db)  # 将 Flask-Migrate 绑定到 Flask 应用和数据库

    # 注册蓝图
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
