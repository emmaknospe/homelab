from api.models.iot_device_setting import IoTDeviceSetting, IoTDeviceSettingValue, IoTDeviceSettingModel


def _setting_type_string(setting: IoTDeviceSetting):
    if setting.value_str is not None:
        return 'str'
    if setting.value_int is not None:
        return 'int'
    if setting.value_float is not None:
        return 'float'
    if setting.value_bool is not None:
        return 'bool'
    raise ValueError('No value set')


def iot_device_setting_to_device_value(setting: IoTDeviceSetting | IoTDeviceSettingModel):
    return IoTDeviceSettingValue(
        device_id=setting.device_id,
        setting_name=setting.setting_name,
        value=setting.value_str or setting.value_int or setting.value_float or setting.value_bool,
        type=_setting_type_string(setting)
    )
