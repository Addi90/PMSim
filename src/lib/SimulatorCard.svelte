<script lang="ts">
  import type { PowerMeterData, Phase, Domain, SimulationType, SimulatorInstance } from './types';
  import { getMeterData, setVoltage, setCurrent, setPower, setSerialNumber, setSimulationPort, setSimulationType, setSimulationState } from './api';
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
  let tempPort = '';
  let serialPorts: string[] = [];
  let hasPhaseChanges = false;
  let hasSettingChanges = false;
  let isLoading = false;

  const simulationTypes: { value: SimulationType; label: string }[] = [
    { value: 'steady', label: 'Steady State' },
    { value: 'fluctuating', label: 'Fluctuating Load' },
    { value: 'overload', label: 'Overload' },
    { value: 'brownout', label: 'Brownout' }
  ];

  // Fetch serial ports on mount
  async function fetchSerialPorts() {
    try {
      const response = await fetch('http://localhost:8000/serial');
      const data = await response.json();
      serialPorts = data.devices;
    } catch (error) {
      console.error('Failed to fetch serial ports:', error);
      serialPorts = [];
    }
  }

  onMount(() => {
    refreshData();
    if (simulator.protocol === 'ModbusRTU') {
      fetchSerialPorts();
    }
    const interval = setInterval(() => {
      if (!hasPhaseChanges && !hasSettingChanges) {
        refreshData();
      }
    }, 1000);

    return () => {
      clearInterval(interval);
    };
  });

  async function refreshData() {
    meterData = await getMeterData(simulator.id);
    tempSerialNumber = meterData.serialNumber;
    tempPort = meterData.port;
    updatePhases();
  }

  function updatePhases() {
    if (!hasPhaseChanges) {
      phases = meterData.voltage.map((_, i) => ({
        voltage: meterData.voltage[i],
        current: meterData.current[i],
        power: meterData.power[i]
      }));
      tempValues = [...meterData[selectedDomain]];
    }
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
      hasSettingChanges = tempSerialNumber !== meterData.serialNumber || tempPort !== meterData.port;
    }
  }

  function handlePortChange(event: Event) {
    const input = event.target as HTMLInputElement;
    tempPort = input.value;
    hasSettingChanges = tempSerialNumber !== meterData.serialNumber || tempPort !== meterData.port;
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
            phases = phases.map((phase, i) => ({
              ...phase,
              voltage: tempValues[i]
            }));
            meterData.voltage = [...tempValues];
            break;
          case 'current':
            await setCurrent(simulator.id, tempValues);
            phases = phases.map((phase, i) => ({
              ...phase,
              current: tempValues[i]
            }));
            meterData.current = [...tempValues];
            break;
          case 'power':
            await setPower(simulator.id, tempValues);
            phases = phases.map((phase, i) => ({
              ...phase,
              power: tempValues[i]
            }));
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
        if (tempPort !== meterData.port) {
          await setSimulationPort(simulator.id, tempPort);
          meterData.port = tempPort;
          simulator.port = tempPort;
        }
      }
      
      setTimeout(async () => {
        await refreshData();
      }, 100);
      
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
  <div class="flex justify-between items-start mb-6 flex-col sm:flex-row gap-4">
    <div>
      <h2 class="text-2xl font-bold text-white">{simulator.protocol}</h2>
      <p class="text-sm text-gray-300">ID: {simulator.id}</p>
    </div>
    
    <div class="flex flex-wrap items-center gap-2 w-full sm:w-auto">
      <div class="flex items-center">
        <span 
          class="status-indicator {simulator.isRunning ? 'running' : 'stopped'}"
          title={simulator.isRunning ? 'Simulator Running' : 'Simulator Stopped'}
        ></span>
        <span class="text-sm text-gray-300 mr-2">
          {simulator.isRunning ? 'Running' : 'Stopped'}
        </span>
      </div>
      
      <select
        class="rounded-none bg-gray-800 border-gray-700 text-white shadow-sm focus:border-blue-500 focus:ring-blue-500 min-w-[150px]"
        value={simulator.simulationType}
        on:change={handleSimulationTypeChange}
      >
        {#each simulationTypes as type}
          <option value={type.value}>{type.label}</option>
        {/each}
      </select>
      
      <div class="flex gap-2 flex-wrap">
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
      <label for="port" class="block text-sm font-medium text-gray-200">
        Port
      </label>
      {#if simulator.protocol === 'ModbusRTU'}
        <select
          id="port"
          class="mt-1 block w-full rounded-none bg-gray-800 border-gray-700 text-white shadow-sm focus:border-blue-500 focus:ring-blue-500"
          value={tempPort}
          on:change={handlePortChange}
        >
          <option value="">Select Port</option>
          {#each serialPorts as port}
            <option value={port}>{port}</option>
          {/each}
        </select>
      {:else}
        <input
          id="port"
          type="text"
          class="mt-1 block w-full rounded-none bg-gray-800 border-gray-700 text-white shadow-sm focus:border-blue-500 focus:ring-blue-500"
          value={tempPort || "502"}
          on:input={handlePortChange}
        />
      {/if}
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