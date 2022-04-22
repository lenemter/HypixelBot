from sqlalchemy import *
from sqlalchemy.orm import relationship
from ..db_session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    music = relationship("Music", back_populates="user")
