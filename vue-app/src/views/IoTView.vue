<!-- IoTDeviceSettingsPage.vue -->
<template>
  <div>
    <h1>IoT Devices</h1>

    <button @click="showModal = true">Create IoT Device</button>
    <IoTDeviceModal :show="showModal" @close="showModal = false" @device-created="onDeviceCreated" />

    <div v-if="loadingDevices">Loading devices...</div>
    <div v-else-if="devicesError">Couldn't retrieve devices: {{ devicesError }}</div>
    <div v-else>
      <label for="deviceSelect">Select a device:</label>
      <select id="deviceSelect" v-model="selectedDeviceId" @change="fetchSettings">
        <option value="">-- Select Device --</option>
        <option v-for="deviceId in deviceIds" :key="deviceId" :value="deviceId">{{ deviceId }}</option>
      </select>
    </div>

    <div v-if="loadingSettings">Loading settings...</div>
    <div v-else-if="settingsError">{{ settingsError }}</div>
    <IoTDeviceSettingsTable v-else-if="settings.length" :settings="settings" />
    <div v-else>No settings available</div>
  </div>
</template>

<script>
import IoTDeviceSettingsTable from '../components/IoTDeviceSettingsTable.vue';
import IoTDeviceModal from '../components/IoTDeviceModal.vue';

export default {
  name: 'IoTDeviceSettingsPage',
  components: {
    IoTDeviceSettingsTable,
    IoTDeviceModal,
  },
  data() {
    return {
      devices: [],
      selectedDeviceId: '',
      settings: [],
      loadingDevices: true,
      devicesError: null,
      loadingSettings: false,
      settingsError: null,
      showModal: false,
    };
  },
  computed: {
    deviceIds() {
      return this.devices.map(device => device.id);
    },
  },
  created() {
    this.fetchDeviceIds();
  },
  methods: {
    async fetchDeviceIds() {
      try {
        const response = await fetch('/api/iot-devices/');
        if (!response.ok) {
          throw new Error('Failed to fetch device IDs');
        }
        this.devices = await response.json();
      } catch (error) {
        this.devicesError = error.message;
      } finally {
        this.loadingDevices = false;
      }
    },
    async fetchSettings() {
      if (!this.selectedDeviceId) {
        this.settings = [];
        return;
      }
      this.loadingSettings = true;
      this.settingsError = null;
      try {
        const response = await fetch(`/api/iot-devices/${this.selectedDeviceId}/settings`);
        if (!response.ok) {
          throw new Error('Failed to fetch settings');
        }
        this.settings = await response.json();
      } catch (error) {
        this.settingsError = error.message;
      } finally {
        this.loadingSettings = false;
      }
    },
    onDeviceCreated() {
      this.fetchDeviceIds();
    },
  },
};
</script>