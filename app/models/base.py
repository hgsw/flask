from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from flask_sqlalchemy.query import Query as _Query
from sqlalchemy import Column, Integer, SmallInteger
from contextlib import contextmanager
from datetime import datetime


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


class Query(_Query):
    """依赖方法的重载，在三方接口上增加'status'默认状态查询条件
    此时还需要将自定义的类替换原有的类"""

    def filter_by(self, **kwargs):
        # print(">>>>>使用自定的查询语句")
        if not "status" in kwargs.keys():
            kwargs["status"] = 1

        return super(Query, self).filter_by(**kwargs)


db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    """__abstract__ = True，该类将作为一个抽象基类使用。
    抽象基类本身并不会映射到数据库中的任何表，它的主要目的是为了被其他模型类继承，从而复用或强制执行一些共同的属性或方法。
    可以定义一些通用的字段或方法，比如创建时间、更新时间、状态字段等，而不用担心这些定义会导致额外的数据库表生成"""

    __abstract__ = True

    create_time = Column("create_time", Integer)
    status = Column(SmallInteger, default=1)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    def set_attrs(self, attrs_dict):
        """动态对传入attrs_dict同名的属性进行复值
        hasattr(object, key)判断对象是否包含key这个属性"""
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != "id":
                setattr(self, key, value)

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        return None

    def delete(self):
        self.status = 0
