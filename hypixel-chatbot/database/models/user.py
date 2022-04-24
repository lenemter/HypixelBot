from sqlalchemy import *
from sqlalchemy.orm import relationship

from ..db_session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    chat_notifiers = relationship("ChatNotifier", back_populates="user")
    news_requests = relationship("NewsRequest", back_populates="user")
    news_stats = relationship("NewsStats", back_populates="user")
    music_requests = relationship("MusicRequest", back_populates="user")
    music_stats = relationship("MusicStats", back_populates="user")
