from . import web
from flask import render_template, request, url_for, redirect, flash
from app.forms.auth import RegisterForm, LoginForm, EmailForm, ResetPasswordForm
from app.models.user import User
from app.models.base import db
from flask_login import login_user, logout_user


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
    form = EmailForm(request.form)
    if request.method == "POST":
        if form.validate():
            account_email = form.email.data
            # first_or_404 遇到查询None会抛出异常，后面的代码不会在执行
            # 这里没有采用是原始的异常抛出，而是在web.__init__中集中处理了404的异常问题
            user = User.query.filter_by(email=account_email).first_or_404()
            from app.libs.email import send_mail

            send_mail(
                account_email, "请重置你的密码", "email/reset_password.html", user=user, token=user.generate_token()
            )
            flash("一封邮件已经发送到邮箱" + account_email + "，请及时查收")
            # return redirect(url_for("web.login"))

    return render_template("auth/forget_password_request.html", form=form)


@web.route("/reset/password/<token>", methods=["GET", "POST"])
def forget_password(token):
    form = ResetPasswordForm(request.form)
    if request.method == "POST" and form.validate():
        success = User.reset_password(token, form.password1.data)
        if success:
            flash("你的密码已更新，请使用新的密码登录")
            return redirect(url_for("web.login"))
        else:
            flash("密码重置失败")
    return render_template("auth/forget_password.html", form=form)


@web.route("/change/password", methods=["GET", "POST"])
def change_password():
    pass


@web.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("web.index"))
