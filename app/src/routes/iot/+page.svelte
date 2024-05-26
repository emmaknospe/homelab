<script>
  let settings = [];
  let newSetting = {
    device_id: '',
    setting_name: '',
    value_str: '',
    value_int: null,
    value_float: null,
    value_bool: null
  };

  async function fetchSettings() {
    const response = await fetch('localhost:8000/api/settings');
    settings = await response.json();
  }

  async function createSetting() {
    const response = await fetch('localhost:8000/api/settings', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(newSetting)
    });

    if (response.ok) {
      await fetchSettings();
      newSetting = {
        device_id: '',
        setting_name: '',
        value_str: '',
        value_int: null,
        value_float: null,
        value_bool: null
      };
    }
  }

  function handleSubmit() {
    createSetting();
  }

  fetchSettings();
</script>

<main>
  <h1>IoT Device Settings</h1>

  <h2>Create Setting</h2>
  <form on:submit|preventDefault={handleSubmit}>
    <label>
      Device ID:
      <input type="text" bind:value={newSetting.device_id} required />
    </label>
    <label>
      Setting Name:
      <input type="text" bind:value={newSetting.setting_name} required />
    </label>
    <label>
      Value (String):
      <input type="text" bind:value={newSetting.value_str} />
    </label>
    <label>
      Value (Integer):
      <input type="number" bind:value={newSetting.value_int} />
    </label>
    <label>
      Value (Float):
      <input type="number" step="any" bind:value={newSetting.value_float} />
    </label>
    <label>
      Value (Boolean):
      <input type="checkbox" bind:checked={newSetting.value_bool} />
    </label>
    <button type="submit">Create</button>
  </form>

  <h2>Settings</h2>
  <ul>
    {#each settings as setting}
      <li>
        <strong>Device ID:</strong> {setting.device_id}<br />
        <strong>Setting Name:</strong> {setting.setting_name}<br />
        <strong>Value (String):</strong> {setting.value_str}<br />
        <strong>Value (Integer):</strong> {setting.value_int}<br />
        <strong>Value (Float):</strong> {setting.value_float}<br />
        <strong>Value (Boolean):</strong> {setting.value_bool}
      </li>
    {/each}
  </ul>
</main>