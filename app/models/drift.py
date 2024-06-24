from app.libs.enums import PendingStatus
from sqlalchemy import Column, String, Integer, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship
from app.models.base import Base


class Drift(Base):
    """一次具体的交易信息"""

    __tablename__ = "drift"

    id = Column(Integer, primary_key=True)
    recipient_name = Column(String(20), nullable=False)
    address = Column(String(100), nullable=False)
    message = Column(String(200))
    mobile = Column(String(20), nullable=False)

    isbn = Column(String(13))
    book_title = Column(String(50))
    book_author = Column(String(30))
    book_img = Column(String(512))
    # requester_id = Column(Integer, ForeignKey('user.id'))
    # requester = relationship('User')
    # 请求者信息
    requester_id = Column(Integer)
    requester_nickname = Column(String(20))
    # 赠送者信息
    gifter_id = Column(Integer)
    gift_id = Column(Integer)
    gifter_nickname = Column(String(20))

    _pending = Column("pending", SmallInteger, default=1)
    # gift_id = Column(Integer, ForeignKey('gift.id'))
    # gift = relationship('Gift')

    @property
    def pending(self):
        # 读取的时将pending转化为枚举
        return PendingStatus(self._pending)

    @pending.setter
    def pending(self, status):
        # 写入时将记录枚举所对应的数字
        self._pending = status.value