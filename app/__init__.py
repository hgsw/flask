from flask import Flask
from app.web import web
from app.models.book import db


def create_app():
    # template_folder 指定模本文件路径
    # app = Flask(__name__, template_folder="web/templates")
    app = Flask(__name__)  # __name__决定当前项目的根目录是/app
    app.config.from_object("app.setting")
    app.config.from_object("app.secure.BaseConfig")
    app.config.from_object("app.secure.Token")

    # 注册路由可在url前面增加路由前缀
    # app.register_blueprint(blueprint=web, url_prefix="/book")
    app.register_blueprint(blueprint=web)
    with app.app_context():
        db.init_app(app)
        db.create_all()

    return app
