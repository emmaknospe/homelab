<template>
  <table class="iot-settings-table">
    <thead>
      <tr>
        <th>Device ID</th>
        <th>Setting Name</th>
        <th>Value</th>
        <th>Type</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="setting in settings" :key="setting.id">
        <td>{{ setting.device_id }}</td>
        <td>{{ setting.setting_name }}</td>
        <td>{{ setting.value }}</td>
        <td>{{ setting.type }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: 'IoTDeviceSettingsTable',
  props: {
    settings: {
      type: Array,
      required: true,
    },
  },
};
</script>
