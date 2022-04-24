from sqlalchemy import *
from sqlalchemy.orm import relationship

from ..db_session import Base


class NewsStats(Base):
    __tablename__ = "news_stats"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="news_stats")

    month = Column(Integer)
    year = Column(Integer)

    count = Column(Integer, nullable=False, default=0)
