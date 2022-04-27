import datetime as dt

from sqlalchemy import *
from sqlalchemy.orm import relationship

from ..db_session import Base


class MusicRequest(Base):
    __tablename__ = "music_requests"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="music_requests")
    datetime = Column(DateTime, nullable=False, default=dt.datetime.now)

    title = Column(String, nullable=False)
