from app.models.base import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from flask import current_app
from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook
from app.models.gift import Gift
from app.models.wish import Wish
from app.models.base import db
from app.models.drift import Drift
from app.libs.enums import PendingStatus
from math import floor


class User(UserMixin, Base):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    _password = Column("password", String(256), nullable=False)
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    def can_send_drift(self):
        """判断能否向他人发起索要书籍"""
        if self.beans < 1:
            return False
        success_gifts_count = Gift.query.filter_by(uid=self.id, launched=True).count()
        success_receive_count = Drift.query.filter_by(requester_id=self.id, pending=PendingStatus.success).count()

        return True if floor(success_receive_count / 2) <= floor(success_gifts_count) else False

    @property
    def summary(self):
        return dict(
            nickname=self.nickname,
            beans=self.beans,
            email=self.email,
            send_receive=str(self.send_counter) + "/" + str(self.receive_counter),
        )

    # 动态设置数据库password密码
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self._password, raw)

    # def get_id(self):
    #     """flask_login 框架验证登录时获取用户的标识
    #     可以从from flask_login import UserMixin继承父类，实现多个方法的重写"""
    #     return self.id

    def can_save_to_list(self, isbn):
        if is_isbn_or_key(isbn) != "isbn":
            return False
        yushu_book = YuShuBook()
        exist = yushu_book.exist_book_by_isbn(isbn)
        if not exist:
            return False

        # 不允许一个用户同时赠送多本相同的图书
        # 一个用户不可能同时成为赠送和索要者

        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()

        if not gifting and not wishing:
            return True
        else:
            return False

    def generate_token(self, expiration=600):
        s = Serializer(current_app.config["SECRET_KEY"], expiration)
        a = s.dumps({"id": self.id}).decode("utf-8")
        print(a)
        return s.dumps({"id": self.id}).decode("utf-8")

    @staticmethod
    def reset_password(token, new_password):
        # token可能过期
        # token可能是别人伪造的
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token.encode("utf-8"))
        except:
            return False

        uid = data.get("id")
        with db.auto_commit():
            user = User.query.get(uid)
            user.password = new_password
        return True
