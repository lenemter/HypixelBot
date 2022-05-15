from sqlalchemy import *

from ..db_session import Base


class UrlCounter(Base):
    __tablename__ = "url_counters"

    id = Column(Integer, primary_key=True)
    base_url = Column(String, nullable=False)
