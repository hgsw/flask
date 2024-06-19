from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from sqlalchemy import Column, Integer, SmallInteger
from contextlib import contextmanager


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


db = SQLAlchemy()


class Base(db.Model):
    """__abstract__ = True，该类将作为一个抽象基类使用。
    抽象基类本身并不会映射到数据库中的任何表，它的主要目的是为了被其他模型类继承，从而复用或强制执行一些共同的属性或方法。
    可以定义一些通用的字段或方法，比如创建时间、更新时间、状态字段等，而不用担心这些定义会导致额外的数据库表生成"""

    __abstract__ = True

    # create_time = Column("create_time", Integer)
    status = Column(SmallInteger, default=1)

    def set_attrs(self, attrs_dict):
        """动态对传入attrs_dict同名的属性进行复值
        hasattr(object, key)判断对象是否包含key这个属性"""
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != "id":
                setattr(self, key, value)
