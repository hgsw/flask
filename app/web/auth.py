from . import web
from flask import render_template, request, url_for, redirect, flash
from app.forms.auth import RegisterForm, LoginForm
from app.models.user import User
from app.models.base import db
from flask_login import login_user


@web.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        with db.auto_commit():  # 使用是with回滚数据库
            user = User()
            # 这里非常重要的思想，动态赋值且考虑到password的处理逻辑
            user.set_attrs(form.data)
            db.session.add(user)
        # db.session.commit()
        return redirect(url_for("web.login"))

    return render_template("auth/register.html", form=form)


@web.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            # 用户票据写入到cookie中
            # login_user是如何知道user模型的用户标识？
            # 这里框架需要实现一个get_id的函数方法。
            # 应用程序验证用户凭证成功后，调用login_user(user) 来记录用户的登录状态
            login_user(user, duration=True)
            # 访问需要登录的界面，登录完成后需要跳转的url地址
            next = request.args.get("next")
            # 需要防止非法的重定向攻击，需要加校验
            if not next or not next.startswith("/"):
                next = url_for("web.index")
            return redirect(next)
        else:
            flash("账号不存在或密码错误")

    return render_template("auth/login.html", form=form)


@web.route("/reset/password", methods=["GET", "POST"])
def forget_password_request():
    pass


@web.route("/reset/password/<token>", methods=["GET", "POST"])
def forget_password(token):
    pass


@web.route("/change/password", methods=["GET", "POST"])
def change_password():
    pass


@web.route("/logout")
def logout():
    pass
