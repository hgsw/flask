from flask import jsonify
from . import web


# 测试web模块不同试视图文件的路由使用
# 实现该功能的关键是蓝图在web包中的init函数中注册
@web.route("/user")
def user():
    """
    测试函数，无其他用途
    """
    return "hello user"
