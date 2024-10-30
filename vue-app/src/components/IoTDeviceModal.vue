<template>
  <div v-if="show" class="modal">
    <div class="modal-content">
      <h2>Create IoT Device</h2>
      <form @submit.prevent="createDevice">
        <div>
          <label for="id">ID:</label>
          <input type="text" id="id" v-model="device.id" required>
        </div>
        <div>
          <label for="name">Name:</label>
          <input type="text" id="name" v-model="device.name" required>
        </div>
        <div>
          <label for="description">Description:</label>
          <textarea id="description" v-model="device.description"></textarea>
        </div>
        <div>
          <label for="deviceType">Device Type:</label>
          <input type="text" id="deviceType" v-model="device.device_type" required>
        </div>
        <div>
          <label for="architecture">Architecture:</label>
          <input type="text" id="architecture" v-model="device.architecture" required>
        </div>
        <div>
          <button type="submit">Create</button>
          <button type="button" @click="closeModal">Cancel</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'IoTDeviceModal',
  props: {
    show: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      device: {
        id: '',
        name: '',
        description: '',
        device_type: '',
        architecture: '',
      },
    };
  },
  methods: {
    createDevice() {
      // Make API call to create the IoT device
      fetch('/api/iot-devices', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(this.device),
      })
        .then(response => {
          if (response.ok) {
            this.closeModal();
            this.$emit('device-created');
          } else {
            console.error('Failed to create IoT device');
          }
        })
        .catch(error => {
          console.error('Error creating IoT device:', error);
        });
    },
    closeModal() {
      this.$emit('close');
    },
  },
};
</script>
