from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey

from api.models.base import Base
from pydantic import BaseModel


class IoTDeviceSettingCreateUpdate(BaseModel):
    device_id: str
    setting_name: str
    value_str: str = None
    value_int: int = None
    value_float: float = None
    value_bool: bool = None

    model_config = {
        'from_attributes': True
    }


class IoTDeviceSetting(IoTDeviceSettingCreateUpdate):
    id: int

    model_config = {
        'from_attributes': True
    }


class IoTDeviceSettingValue(BaseModel):
    device_id: str
    setting_name: str
    value: str | int | float | bool
    type: str

    model_config = {
        'from_attributes': True
    }


class IoTDeviceSettingModel(Base):
    __tablename__ = 'iot_device_settings'

    id: int = Column(Integer, primary_key=True, index=True)
    device_id: str = ForeignKey('iot_devices.id')
    setting_name: str = Column(String)
    value_str: str = Column(String, nullable=True)
    value_int: int = Column(Integer, nullable=True)
    value_float: float = Column(Float, nullable=True)
    value_bool: bool = Column(Boolean, nullable=True)

    model_config = {
        'from_attributes': True
    }
