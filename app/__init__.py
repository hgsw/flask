from flask import Flask
from app.web import web
from app.models.book import db


def create_app():
    app = Flask(__name__)
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
