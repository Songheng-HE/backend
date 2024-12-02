from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # 导入CORS
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)  # 启用CORS

    # 获取当前文件（__init__.py）的绝对路径
    base_dir = os.path.abspath(os.path.dirname(__file__))

    # 配置数据库的绝对路径
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'game_assistant.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
