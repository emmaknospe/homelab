from api.models.iot_device_setting import \
    IoTDeviceSetting, \
    IoTDeviceSettingCreateUpdate, \
    IoTDeviceSettingModel

from api.utils.crud import CRUDRouter


iot_device_settings_router = CRUDRouter(
    model=IoTDeviceSetting,
    create_model=IoTDeviceSettingCreateUpdate,
    update_model=IoTDeviceSettingCreateUpdate,
    sql_model=IoTDeviceSettingModel,
    prefix="/iot-device-settings"
)
