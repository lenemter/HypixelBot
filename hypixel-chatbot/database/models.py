import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class News(SqlAlchemyBase):
    __tablename__ = "news"

    id = sqlalchemy.Column(
        sqlalchemy.Integer, nullable=False, unique=True, primary_key=True
    )
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    link = sqlalchemy.Column(sqlalchemy.String, nullable=False)


class Reminders(SqlAlchemyBase):
    __tablename__ = "reminders"

    id = sqlalchemy.Column(
        sqlalchemy.Integer, nullable=False, unique=True, primary_key=True
    )
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    link = sqlalchemy.Column(sqlalchemy.String, nullable=False)