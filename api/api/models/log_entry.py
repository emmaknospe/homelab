from sqlalchemy import Column, Integer, String

from api.models.base import Base
from pydantic import BaseModel


class LogEntryCreateUpdate(BaseModel):
    device_id: str
    log_level: str
    log_stream: str
    message: str

    model_config = {
        'from_attributes': True
    }


class LogEntry(LogEntryCreateUpdate):
    id: int

    model_config = {
        'from_attributes': True
    }


class LogEntryModel(Base):
    __tablename__ = 'log_entries'

    id = Column(Integer, primary_key=True)
    device_id = Column(String)
    log_level = Column(String)
    log_stream = Column(String)
    message = Column(String)

    model_config = {
        'from_attributes': True
    }
