from . import web
from flask_login import login_required


@web.route("/my/gifts")
@login_required
def my_gifts():
    """@login_required用于授权登录
    但是需要@login_manager.user_loader装饰函数返回的user对象"""
    return "gifts"


@web.route("/gifts/book/<isbn>")
def save_to_gifts(isbn):
    pass


@web.route("/gifts/<gid>/redraw")
def redraw_from_gifts(gid):
    pass
