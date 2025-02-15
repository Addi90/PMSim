<script lang="ts">
  import { onMount } from 'svelte';
  import type { PowerMeterData, Phase, Domain } from './lib/types';
  import { getMeterData, setVoltage, setCurrent, setPower, setSerialNumber, setBrand } from './lib/api';
  import PhaseCard from './lib/PhaseCard.svelte';

  let meterData: PowerMeterData = {
    voltage: [0, 0, 0],
    current: [0, 0, 0],
    power: [0, 0, 0],
    serialNumber: '',
    brand: 'Brand1'
  };

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

  onMount(async () => {
    await refreshData();
  });

  async function refreshData() {
    meterData = await getMeterData();
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

  async function applyChanges() {
    if ((!hasPhaseChanges && !hasSettingChanges) || isLoading) return;

    try {
      isLoading = true;
      
      if (hasPhaseChanges) {
        switch (selectedDomain) {
          case 'voltage':
            await setVoltage(tempValues);
            meterData.voltage = [...tempValues];
            break;
          case 'current':
            await setCurrent(tempValues);
            meterData.current = [...tempValues];
            break;
          case 'power':
            await setPower(tempValues);
            meterData.power = [...tempValues];
            break;
        }
      }

      if (hasSettingChanges) {
        if (tempSerialNumber !== meterData.serialNumber) {
          await setSerialNumber(tempSerialNumber);
          meterData.serialNumber = tempSerialNumber;
        }
        if (tempBrand !== meterData.brand) {
          await setBrand(tempBrand);
          meterData.brand = tempBrand;
        }
      }
      
      await refreshData();
      hasPhaseChanges = false;
      hasSettingChanges = false;
    } catch (error) {
      console.error('Failed to apply changes:', error);
      // Reset to original values on error
      await refreshData();
    } finally {
      isLoading = false;
    }
  }
</script>

<main class="min-h-screen py-8 px-4">
  <div class="max-w-6xl mx-auto">
    <div class="glass-dark p-8 rounded-lg mb-8">
      <h1 class="text-3xl font-bold text-white mb-8">Power Meter Simulation</h1>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div>
          <label for="serialNumber" class="block text-sm font-medium text-gray-200">
            Serial Number (7 digits)
          </label>
          <input
            id="serialNumber"
            type="text"
            maxlength="7"
            pattern="\d*"
            class="mt-1 block w-full rounded-none bg-gray-800 border-gray-700 text-white shadow-sm focus:border-blue-500 focus:ring-blue-500"
            value={tempSerialNumber}
            on:input={handleSerialNumberChange}
          />
        </div>
        
        <div>
          <label for="brand" class="block text-sm font-medium text-gray-200">
            Brand
          </label>
          <select
            id="brand"
            class="mt-1 block w-full rounded-none bg-gray-800 border-gray-700 text-white shadow-sm focus:border-blue-500 focus:ring-blue-500"
            value={tempBrand}
            on:change={handleBrandChange}
          >
            <option value="Brand1">Brand 1</option>
            <option value="Brand2">Brand 2</option>
          </select>
        </div>

        <div>
          <label for="domain" class="block text-sm font-medium text-gray-200">
            Edit Mode
          </label>
          <select
            id="domain"
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
    </div>

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

    <div class="w-full px-4 md:px-0">
      <button
        class="w-full h-16 bg-blue-600 text-white text-lg font-semibold rounded-none hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200 glass"
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
    </div>
  </div>
</main>