from flask import Flask
from app.web import web

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.setting")
    app.config.from_object("app.secure")
    
    # 注册路由可在url前面增加路由前缀
    # app.register_blueprint(blueprint=web, url_prefix="/book")
    app.register_blueprint(blueprint=web)
    return app

