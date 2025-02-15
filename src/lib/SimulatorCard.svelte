<script lang="ts">
  import type { PowerMeterData, Phase, Domain, SimulationType, SimulatorInstance } from './types';
  import { getMeterData, setVoltage, setCurrent, setPower, setSerialNumber, setBrand, setSimulationType, setSimulationState } from './api';
  import { onMount } from 'svelte';
  import PhaseCard from './PhaseCard.svelte';

  export let simulator: SimulatorInstance;
  export let onRemove: (id: string) => void;

  let meterData: PowerMeterData;
  let phases: Phase[] = [
    { voltage: 0, current: 0, power: 0 },
    { voltage: 0, current: 0, power: 0 },
    { voltage: 0, current: 0, power: 0 }
  ];

  let selectedDomain: Domain = 'power';
  let tempValues: [number, number, number] = [0, 0, 0];
  let tempSerialNumber = '';
  let tempBrand: 'Brand1' | 'Brand2' = 'Brand1';
  let hasPhaseChanges = false;
  let hasSettingChanges = false;
  let isLoading = false;

  const simulationTypes: { value: SimulationType; label: string }[] = [
    { value: 'steady', label: 'Steady State' },
    { value: 'fluctuating', label: 'Fluctuating Load' },
    { value: 'overload', label: 'Overload' },
    { value: 'brownout', label: 'Brownout' }
  ];

  // call refreshData() when the component is mounted and refresh every second
  onMount(async () => {
    await refreshData();
    setInterval(async () => {
      await refreshData();
    }, 1000);
  });

  async function refreshData() {
    meterData = await getMeterData(simulator.id);
    tempSerialNumber = meterData.serialNumber;
    tempBrand = meterData.brand;
    updatePhases();
  }

  function updatePhases() {
    phases = meterData.voltage.map((_, i) => ({
      voltage: meterData.voltage[i],
      current: meterData.current[i],
      power: meterData.power[i]
    }));
    tempValues = [...meterData[selectedDomain]];
  }

  function handlePhaseUpdate(phaseIndex: number, value: number) {
    tempValues[phaseIndex] = value;
    hasPhaseChanges = true;
  }

  function handleSerialNumberChange(event: Event) {
    const input = event.target as HTMLInputElement;
    const value = input.value;
    
    if (value.length <= 7 && /^\d*$/.test(value)) {
      tempSerialNumber = value;
      hasSettingChanges = tempSerialNumber !== meterData.serialNumber || tempBrand !== meterData.brand;
    }
  }

  function handleBrandChange(event: Event) {
    const select = event.target as HTMLSelectElement;
    tempBrand = select.value as 'Brand1' | 'Brand2';
    hasSettingChanges = tempSerialNumber !== meterData.serialNumber || tempBrand !== meterData.brand;
  }

  function handleDomainChange(event: Event) {
    const select = event.target as HTMLSelectElement;
    selectedDomain = select.value as Domain;
    tempValues = [...meterData[selectedDomain]];
    hasPhaseChanges = false;
  }

  async function handleSimulationTypeChange(event: Event) {
    const select = event.target as HTMLSelectElement;
    const type = select.value as SimulationType;
    await setSimulationType(simulator.id, type);
    simulator.simulationType = type;
  }

  async function toggleSimulation() {
    const newState = !simulator.isRunning;
    await setSimulationState(simulator.id, newState);
    simulator.isRunning = newState;
  }

  async function applyChanges() {
    if ((!hasPhaseChanges && !hasSettingChanges) || isLoading) return;

    try {
      isLoading = true;
      
      if (hasPhaseChanges) {
        switch (selectedDomain) {
          case 'voltage':
            await setVoltage(simulator.id, tempValues);
            meterData.voltage = [...tempValues];
            break;
          case 'current':
            await setCurrent(simulator.id, tempValues);
            meterData.current = [...tempValues];
            break;
          case 'power':
            await setPower(simulator.id, tempValues);
            meterData.power = [...tempValues];
            break;
        }
      }

      if (hasSettingChanges) {
        if (tempSerialNumber !== meterData.serialNumber) {
          await setSerialNumber(simulator.id, tempSerialNumber);
          meterData.serialNumber = tempSerialNumber;
          simulator.serialNumber = tempSerialNumber;
        }
        if (tempBrand !== meterData.brand) {
          await setBrand(simulator.id, tempBrand);
          meterData.brand = tempBrand;
          simulator.brand = tempBrand;
        }
      }
      
      await refreshData();
      hasPhaseChanges = false;
      hasSettingChanges = false;
    } catch (error) {
      console.error('Failed to apply changes:', error);
      await refreshData();
    } finally {
      isLoading = false;
    }
  }

</script>

<div class="glass p-6 rounded-lg mb-8">
  <div class="flex justify-between items-start mb-6">
    <div>
      <h2 class="text-2xl font-bold text-white">{simulator.protocol}</h2>
      <p class="text-sm text-gray-300">ID: {simulator.id}</p>
    </div>
    <div class="flex items-center gap-4">
      <select
        class="rounded-none bg-gray-800 border-gray-700 text-white shadow-sm focus:border-blue-500 focus:ring-blue-500"
        value={simulator.simulationType}
        on:change={handleSimulationTypeChange}
      >
        {#each simulationTypes as type}
          <option value={type.value}>{type.label}</option>
        {/each}
        
      </select>
      <button
        class="px-4 h-10 {simulator.isRunning ? 'bg-red-600 hover:bg-red-700' : 'bg-green-600 hover:bg-green-700'} text-white font-semibold rounded-none transition-colors duration-200 glass"
        on:click={toggleSimulation}
      >
        {simulator.isRunning ? 'Stop' : 'Start'}
      </button>
      <button
        class="px-4 h-10 bg-red-600 hover:bg-red-700 text-white font-semibold rounded-none transition-colors duration-200 glass"
        on:click={() => onRemove(simulator.id)}
      >
        Remove
      </button>
    </div>
  </div>

  <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
    <div>
      <label for="serial-number" class="block text-sm font-medium text-gray-200">
        Serial Number (7 digits)
      </label>
      <input
        id="serial-number"
        type="text"
        maxlength="7"
        pattern="\d*"
        class="mt-1 block w-full rounded-none bg-gray-800 border-gray-700 text-white shadow-sm focus:border-blue-500 focus:ring-blue-500"
        value={tempSerialNumber}
        on:input={handleSerialNumberChange}
      />
    </div>

    <div>
      <label for="edit-mode" class="block text-sm font-medium text-gray-200">
        Edit Mode
      </label>
      <select
        id="edit-mode"
        class="mt-1 block w-full rounded-none bg-gray-800 border-gray-700 text-white shadow-sm focus:border-blue-500 focus:ring-blue-500"
        value={selectedDomain}
        on:change={handleDomainChange}
      >
        <option value="power">Power</option>
        <option value="voltage">Voltage</option>
        <option value="current">Current</option>
      </select>
    </div>
  </div>

  {#if meterData}
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      {#each phases as phase, i}
        <PhaseCard
          {phase}
          phaseNumber={i + 1}
          {selectedDomain}
          onUpdate={(value) => handlePhaseUpdate(i, value)}
        />
      {/each}
      
    </div>

    <button
      class="w-full h-12 bg-blue-600 text-white text-lg font-semibold rounded-none hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200 glass"
      on:click={applyChanges}
      disabled={(!hasPhaseChanges && !hasSettingChanges) || isLoading}
    >
      {#if isLoading}
        Applying Changes...
      {:else if hasPhaseChanges || hasSettingChanges}
        Apply Changes
      {:else}
        No Changes to Apply
      {/if}
      
    </button>
  {/if}
  
</div>