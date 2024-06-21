from app.models.base import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, desc
from sqlalchemy.orm import relationship
from app.models.base import db
from flask import current_app
from app.spider.yushu_book import YuShuBook
from sqlalchemy.sql import func, and_


class Gift(Base):

    __tablename__ = "gift"

    id = Column(Integer, primary_key=True)
    user = relationship("User")
    uid = Column(Integer, ForeignKey("user.id"))
    isbn = Column(String(15), nullable=False)
    # book = relationship("Book")
    # bid = Column(Integer, ForeignKey("book.id"))
    launched = Column(Boolean, default=False)

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
