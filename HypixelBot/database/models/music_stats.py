from sqlalchemy import *
from sqlalchemy.orm import relationship

from ..db_session import Base


class MusicStats(Base):
    __tablename__ = "music_stats"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="music_stats")

    title = Column(String, nullable=False)
    month = Column(Integer)
    year = Column(Integer)

    count = Column(Integer, nullable=False, default=0)
