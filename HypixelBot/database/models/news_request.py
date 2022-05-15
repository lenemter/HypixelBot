import datetime as dt

from sqlalchemy import *
from sqlalchemy.orm import relationship

from ..db_session import Base


class NewsRequest(Base):
    __tablename__ = "news_requests"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="news_requests")
    datetime = Column(DateTime, nullable=False, default=dt.datetime.now)

    count = Column(Integer, nullable=False)
