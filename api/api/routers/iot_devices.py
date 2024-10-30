from fastapi import Depends
from sqlalchemy.orm import Session

from api.models.iot_device import IoTDevice, IoTDeviceUpdate, IoTDeviceModel
from api.models.iot_device_setting import IoTDeviceSettingModel, IoTDeviceSetting
from api.utils.iot import iot_device_setting_to_device_value
from api.utils.crud import CRUDRouter
from db import get_db

iot_devices_router = CRUDRouter(
    model=IoTDevice,
    create_model=IoTDevice,
    update_model=IoTDeviceUpdate,
    sql_model=IoTDeviceModel,
    prefix="/iot-devices"
)


@iot_devices_router.get(
    "/{device_id}/settings",
    response_model=IoTDeviceSetting,
    response_model_exclude_unset=True,
)
async def get_iot_device_settings_by_device_id(device_id: str, db: Session = Depends(get_db)):
    matching_settings = db.query(IoTDeviceSettingModel).filter(IoTDeviceSettingModel.device_id == device_id).all()
    return [
        iot_device_setting_to_device_value(setting)
        for setting in matching_settings
    ]
