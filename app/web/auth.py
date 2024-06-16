from . import web
from flask import render_template, request, url_for, redirect
from app.forms.auth import RegisterForm, LoginForm
from app.models.user import User
from app.models.base import db


@web.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        user = User()
        # 这里非常重要的思想，动态赋值且考虑到password的处理逻辑
        user.set_attrs(form.data)
        db.session.add(user)
        db.session.commit()

    return render_template("auth/register.html", form=form)


@web.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate():
        pass

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
