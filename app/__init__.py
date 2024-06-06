from flask import Flask
from app.web.book import web


def create_app():
    app = Flask(__name__)
    app.config.from_object("config")
    # 将web.book的视图函数文件以蓝图的当时注册到时flask中
    app.register_blueprint(web)

    return app
