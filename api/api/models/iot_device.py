from sqlalchemy import Column, String

from api.models.base import Base
from pydantic import BaseModel


class IoTDeviceUpdate(BaseModel):
    name: str
    description: str
    device_type: str
    architecture: str

    model_config = {
        'from_attributes': True
    }


class IoTDevice(IoTDeviceUpdate):
    id: str

    model_config = {
        'from_attributes': True
    }


class IoTDeviceModel(Base):
    __tablename__ = 'iot_devices'

    id: str = Column(String, primary_key=True, index=True, unique=True, autoincrement=False)
    name: str = Column(String)
    description: str = Column(String, nullable=True)
    device_type: str = Column(String)
    architecture: str = Column(String)

    model_config = {
        'from_attributes': True
    }
