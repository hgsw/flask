from flask import Flask
from flask_login import LoginManager
from app.web import web
from app.models.base import db
from app.models.user import User

login_manager = LoginManager()


# @login_manager.user_loader
# 每个请求开始时（如果需要的话），根据会话中存储的用户id重新加载用户对象
# Flask-Login使用这个函数来恢复一个已经登录的用户的完整对象实例，以便在整个请求生命周期中使用
@login_manager.user_loader
def load_user(user_id):
    # user = db.session.query(User).get(user_id)
    user = User.query.get(int(user_id))
    return user


def create_app():
    # template_folder 指定模本文件路径
    # app = Flask(__name__, template_folder="web/templates")
    app = Flask(__name__)  # __name__决定当前项目的根目录是/app
    app.config.from_object("app.setting")
    app.config.from_object("app.secure.BaseConfig")
    app.config.from_object("app.secure.Token")
    app.config["SQLALCHEMY_ECHO"] = True  # 启用SQL语句的打印

    # 注册路由可在url前面增加路由前缀
    # app.register_blueprint(blueprint=web, url_prefix="/book")
    app.register_blueprint(blueprint=web)
    login_manager.init_app(app)
    # 当访问需要登录的页面，这里可以定义跳转登录的界面
    login_manager.login_view = "web.login"
    login_manager.login_message = "请先登录或注册"
    with app.app_context():
        db.init_app(app)
        db.create_all()

    return app
