from sqlalchemy import *
from sqlalchemy.orm import relationship

from ..db_session import Base


class ChatNotifier(Base):
    __tablename__ = "chat_notifiers"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="chat_notifiers")

    channel_id = Column(Integer, nullable=False)
