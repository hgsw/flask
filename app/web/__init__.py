from flask import Blueprint, render_template

# 视图模块解耦，每个视图模块都在init函数中进行蓝图注册
# __name__ 表明蓝图所在的模块，当前文件__name__=app.web
web = Blueprint("web", __name__)


# 统一处理了404的异常
@web.app_errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


# 表面上这个web像循环导入，实际上只执行一次
from app.web import book
from app.web import user
from app.web import auth
from app.web import drift
from app.web import gift
from app.web import main
from app.web import wish
