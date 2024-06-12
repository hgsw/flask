from flask import Flask, current_app

"""
flask 的上下文
1、应用上下文 flask 的封装
2、请求上下文 request 的封装
Flask 对象在 AppContext中
Request 对象在 RequestContext中 

如果需要使用Flask或Request对象，需要从对应的上下文中间接获取对象。
"""

app = Flask(__name__)
print(f"原始app内存地址：{id(app)}")

""" 这里直接报错 RuntimeError: Working outside of application context.
原因：这里只是创建一个app对象，我们需要手动将这个flask对象加入到应用上下文中
请注意：在视图函数或路由处理程序中：当你定义一个路由并注册一个视图函数时，
flask会在处理HTTP请求时自动激活应用上下文和请求上下文
因此你可以在这些函数内部安全地访问current_app或request对象。

下面代码中的app_context 和 current_app不是一回事，需要慢慢体会"""

# d = current_app.config["DEBUG"]
# print(d)


# 手动将app对象加到应用上下文中
ctx = app.app_context()
ctx.push()  # 此时debug时，可以看到current_app不再是空
# app_context有一个app属性，可以和开始创建的app进行比较
print(f"app_context中的app内存地址：{id(ctx.app)}")
# app_context 应用上下文地址
print(f"app_context的内存地址：{id(ctx)}")

# current_app是一个本地代理内存地址和app的内存地址不一样但功能是一样
print(f"current_app的内存地址：{id(current_app)}")
# 可以正确访问
d = current_app.config["DEBUG"]
print(d)
# 需要清除应用上下文
ctx.pop()

# 推荐用法
with app.app_context():
    d = current_app.config["DEBUG"]
    print(d)
