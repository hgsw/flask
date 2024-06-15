from app.models.base import db
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class Gift(db.Model):
    __tablename__ = "gift"

    id = Column(Integer, primary_key=True)
    user = relationship("User")
    uid = Column(Integer, ForeignKey("user.id"))
    isbn = Column(String(15), nullable=False)
    # book = relationship("Book")
    # bid = Column(Integer, ForeignKey("book.id"))
    launched = Column(Boolean, default=False)
