<script lang="ts">
  import { onMount } from 'svelte';
  import type { SimulatorProtocol, SimulatorInstance } from './lib/types';
  import { getSimulatorConfig, addSimulator, removeSimulator, resetConfig } from './lib/api';
  import SimulatorCard from './lib/SimulatorCard.svelte';

  let simulators: SimulatorInstance[] = [];
  let selectedProtocol: SimulatorProtocol = 'ModbusRTU';

  const protocolOptions: { value: SimulatorProtocol; label: string }[] = [
    { value: 'ModbusRTU', label: 'Modbus RTU' },
    { value: 'ModbusTCP', label: 'Modbus TCP' }
  ];

  onMount(async () => {
    await refreshSimulators();
    // Start polling for updates
    setInterval(async () => {
      await refreshSimulators();
    }, 1000);
  });

  async function refreshSimulators() {
    const config = await getSimulatorConfig();
    simulators = config.instances;
  }

  async function handleAddSimulator() {
    await addSimulator(selectedProtocol);
    await refreshSimulators();
  }

  async function handleRemoveSimulator(id: string) {
    await removeSimulator(id);
    await refreshSimulators();
  }

  async function handleResetConfig() {
    await resetConfig();
    await refreshSimulators();
  }
</script>

<main class="min-h-screen py-8 px-4">
  <div class="max-w-6xl mx-auto">
    <div class="glass-dark p-8 rounded-lg mb-8">
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-8">
        <h1 class="text-3xl font-bold text-white">Power Meter Simulation</h1>
        <div class="flex flex-col md:flex-row items-start md:items-center gap-4">
          <div class="flex items-center gap-2">
            <select
              class="rounded-none bg-gray-800 border-gray-700 text-white shadow-sm focus:border-blue-500 focus:ring-blue-500"
              bind:value={selectedProtocol}
            >
              {#each protocolOptions as option}
                <option value={option.value}>{option.label}</option>
              {/each}
              
            </select>
            <button
              class="px-4 h-10 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-none transition-colors duration-200 glass"
              on:click={handleAddSimulator}
            >
              Add Simulator
            </button>
          </div>
          <button
            class="px-4 h-10 bg-red-600 hover:bg-red-700 text-white font-semibold rounded-none transition-colors duration-200 glass"
            on:click={handleResetConfig}
          >
            Reset All
          </button>
        </div>
      </div>
    </div>

    {#each simulators as simulator (simulator.id)}
      <SimulatorCard
        {simulator}
        onRemove={handleRemoveSimulator}
      />
    {/each}
    
  </div>
</main>