from flask import Blueprint

web = Blueprint("web", __name__)  # __name__ 表明蓝图所在的模块，当前文件

# 表面上这个web像循环导入，实际上只执行一次
from app.web import book
from app.web import user
