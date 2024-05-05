from sqlalchemy import Column, Integer, String

from api.models.base import Base


class LogEntry(Base):
    __tablename__ = 'log_entries'

    id = Column(Integer, primary_key=True)
    message = Column(String)
