from collections.abc import Sequence
from typing import Any, Mapping
from wtforms import Form, StringField, PasswordField
from wtforms.validators import Length, DataRequired, Email, ValidationError, EqualTo
from app.models.user import User


class RegisterForm(Form):
    email = StringField(validators=[DataRequired(), Length(min=8, max=64), Email(message="电子邮箱不符合规范")])
    password = PasswordField(validators=[DataRequired(message="密码不可以为空，请输入你的密码"), Length(6, 32)])
    nickname = StringField(validators=[DataRequired(), Length(2, 10, message="昵称最少两个字符，最多10个字符")])

    # 自定义业务校验器， field框架自己传入，错误会保存在form.errors里面
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("电子邮箱已被注册")

    def validate_nickname(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("昵称已被注册")


class LoginForm(Form):
    email = StringField(validators=[DataRequired(), Length(min=8, max=64), Email(message="电子邮箱不符合规范")])
    # nickname = StringField(validators=[DataRequired(), Length(2, 10, message="昵称最少两个字符，最多10个字符")])
    password = PasswordField(validators=[DataRequired(message="密码不可以为空，请输入你的密码"), Length(6, 32)])


class EmailForm(Form):
    email = StringField(validators=[DataRequired(), Length(min=8, max=64), Email(message="电子邮箱不符合规范")])


class ResetPasswordForm(Form):
    password1 = PasswordField(
        validators=[
            DataRequired(),
            Length(6, 32, "密码长度需要在6到32个字符之间，不可以为空"),
            EqualTo("password2", "两次输入的密码不相同"),
        ]
    )
    password2 = PasswordField(validators=[DataRequired(), Length(6, 32)])
