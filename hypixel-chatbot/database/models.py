from sqlalchemy import *
from sqlalchemy.orm import relationship
from .db_session import Base


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    link = Column(String, nullable=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)


class Music(Base):
    __tablename__ = "music"

    id = Column(Integer, primary_key=True)
    user = relationship("Users")
