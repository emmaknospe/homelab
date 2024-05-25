from fastapi import Depends
from sqlalchemy.orm import Session

from api.models.iot_device_setting import \
    IoTDeviceSetting, \
    IoTDeviceSettingCreateUpdate, \
    IoTDeviceSettingModel

from api.utils.crud import CRUDRouter
from db import get_db

iot_device_settings_router = CRUDRouter(
    model=IoTDeviceSetting,
    create_model=IoTDeviceSettingCreateUpdate,
    update_model=IoTDeviceSettingCreateUpdate,
    sql_model=IoTDeviceSettingModel,
    prefix="/iot-device-settings"
)


@iot_device_settings_router.get(
    "/by-device-id/{device_id}",
    response_model=IoTDeviceSetting,
    response_model_exclude_unset=True,
)
async def get_iot_device_setting_by_device_id(device_id: str, db: Session = Depends(get_db)):
    matching_settings = db.query(IoTDeviceSettingModel).filter(IoTDeviceSettingModel.device_id == device_id).all()
    return [
        IoTDeviceSetting.model_validate(setting) for setting in matching_settings
    ]
