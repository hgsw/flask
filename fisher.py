from flask import Flask, make_response

app = Flask(__name__)
# 入参config是模块名
# from_object 要求配置文件里面的所有变量需要全部大写
app.config.from_object("config")

# print(app.config["DEBUG"])


# rul兼容/和不带/  重定向 301或302
@app.route("/hello")
def hello():
    # flask 会做一些封装 status、content-type(默认值 text/html; charset=utf-8)
    return "路由/hello不兼容/，访问/hello/ 返回404"


# rul兼容/和不带/  重定向 301或302
@app.route("/hello2/")
def hello2():
    # flask 会做一些封装 status、content-type(默认值 text/html; charset=utf-8)
    return "路由/hello2兼容/，访问/hello2会重定向到/hello2/"


@app.route("/hello3")
def hello3():
    # flask 会做一些封装 http status、content-type(默认值 text/html; charset=utf-8)
    header = {"content-type": "text/plain"}
    response = make_response("<html>blue<html>", 200)
    response.headers = header
    return response


# app.add_url_rule("/hello", view_func=hello)   # 通过这种方式也可以注册路由和视图函数

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=app.config["DEBUG"])
