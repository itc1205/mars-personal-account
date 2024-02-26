from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Boolean
from sqlalchemy.orm import relation
from datetime import datetime as dt

from .db_session import SqlAlchemyBase


class Job(SqlAlchemyBase):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)

    leader_id = Column(Integer, ForeignKey("users.id"))
    leader = relation("User")

    job = Column(String)
    work_size = Column(Integer)
    collaborators = Column(String)
    start_date = Column(DateTime, default=dt.now)
    end_date = Column(DateTime)
    is_finished = Column(Boolean)
