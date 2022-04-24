from sqlalchemy import *
from sqlalchemy.orm import relationship

from ..db_session import Base


class Music(Base):
    __tablename__ = "music"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="music")

    title = Column(String, nullable=False)
    month = Column(Integer)
    year = Column(Integer)

    count = Column(Integer, nullable=False, default=0)
