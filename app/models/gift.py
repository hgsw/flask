from app.models.base import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, desc, func
from sqlalchemy.orm import relationship
from app.models.base import db
from app.models.wish import Wish
from flask import current_app
from app.spider.yushu_book import YuShuBook
from sqlalchemy.sql import func, and_
from collections import namedtuple

# 快速定义一个类
EachGiftWishCount = namedtuple("EachGiftWishCount", ["count", "isbn"])


class Gift(Base):

    __tablename__ = "gift"

    id = Column(Integer, primary_key=True)
    user = relationship("User")
    uid = Column(Integer, ForeignKey("user.id"))
    isbn = Column(String(15), nullable=False)
    # book = relationship("Book")
    # bid = Column(Integer, ForeignKey("book.id"))
    launched = Column(Boolean, default=False)

    @classmethod
    def get_user_gifts(cls, uid):
        """根据当前用户id查询所有的赠送清单"""
        gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(desc(Gift.create_time)).all()
        return gifts

    @classmethod
    def get_wish_counts(cls, isbn_lst):
        """根据一组isbn到wish表中查询礼物的wish的心愿数量"""
        # db.session.query(Wish).filter(Wish.launched == False, Wish.isbn.in_(isbn_lst), Wish.status == 1).all()

        # 分组统计
        count_lst = (
            db.session.query(func.count(Wish.id), Wish.isbn)
            .filter(Wish.launched == False, Wish.isbn.in_(isbn_lst), Wish.status == 1)
            .group_by(Wish.isbn)
            .all()
        )
        # print(count_lst)  # [(1, '9787115545138'), (1, '9787501524044')]
        # 直接构造一个字典进行返回
        count_lst = [{"count": w[0], "isbn": w[1]} for w in count_lst]
        # 不要返回元组，推荐返回dict
        return count_lst

    # @classmethod
    # def get_wish_counts(cls, isbn_lst):

    #     count_lst = (
    #         db.session.query(func.count(Wish.id), Wish.isbn)
    #         .filter(Wish.launched == False, Wish.isbn.in_(isbn_lst), Wish.status == 1)
    #         .group_by(Wish.isbn)
    #         .all()
    #     )
    #     count_lst = [EachGiftWishCount(w[0], w[1]) for w in count_lst]
    #     return count_lst

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    @classmethod
    def recent(cls):
        """查询最新的30条，需要排序，需要去重"""
        # recent_gift = (
        #     Gift.query.filter_by(launched=False)
        #     .group_by(Gift.isbn)
        #     .order_by(Gift.create_time)
        #     .limit(current_app.config["RECENT_BOOK_COUNT"])
        #     .distinct()
        #     .all()
        # )

        subquery = (
            Gift.query.with_entities(Gift.isbn, func.max(Gift.create_time).label("max_create_time"))
            .filter(Gift.launched == False)
            .group_by(Gift.isbn)
            .subquery()
        )
        recent_gifts = (
            Gift.query.filter(and_(Gift.isbn == subquery.c.isbn, Gift.create_time == subquery.c.max_create_time))
            .order_by(Gift.create_time.desc())
            .distinct(Gift.isbn)
            .limit(current_app.config["RECENT_BOOK_COUNT"])
            .all()
        )
        # print(recent_gifts)

        return recent_gifts
