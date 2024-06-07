from flask import Blueprint

# 视图模块解耦，每个视图模块都在init函数中进行蓝图注册
# __name__ 表明蓝图所在的模块，当前文件__name__=app.web
web = Blueprint("web", __name__)  

# 表面上这个web像循环导入，实际上只执行一次
from app.web import book
from app.web import user
