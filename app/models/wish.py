from app.models.base import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import desc, and_, func
from app.models.base import db
from app.spider.yushu_book import YuShuBook


class Wish(Base):

    __tablename__ = "wish"

    id = Column(Integer, primary_key=True)
    user = relationship("User")
    uid = Column(Integer, ForeignKey("user.id"))
    isbn = Column(String(15), nullable=False)
    # book = relationship("Book")
    # bid = Column(Integer, ForeignKey("book.id"))
    launched = Column(Boolean, default=False)

    @classmethod
    def get_user_wishes(cls, uid):
        """根据当前用户id查询所有的心愿清单"""
        wishes = Wish.query.filter_by(uid=uid, launched=False).order_by(desc(Wish.create_time)).all()
        return wishes

    @classmethod
    def get_gift_counts(cls, isbn_lst):
        from app.models.gift import Gift
        # 分组统计
        count_lst = (
            db.session.query(func.count(Gift.id), Gift.isbn)
            .filter(Gift.launched == False, Gift.isbn.in_(isbn_lst), Gift.status == 1)
            .group_by(Gift.isbn)
            .all()
        )
        # 直接构造一个字典进行返回
        count_lst = [{"count": w[0], "isbn": w[1]} for w in count_lst]
        # 不要返回元组，推荐返回dict
        return count_lst

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first
