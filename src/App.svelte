<script lang="ts">
  import { onMount } from 'svelte';
  import type { PowerMeterData, Phase } from './lib/types';
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

  onMount(async () => {
    meterData = await getMeterData();
    updatePhases();
  });

  function updatePhases() {
    phases = meterData.voltage.map((_, i) => ({
      voltage: meterData.voltage[i],
      current: meterData.current[i],
      power: meterData.power[i]
    }));
  }

  async function handlePhaseUpdate(phaseIndex: number, field: keyof Phase, value: number) {
    const values = phases.map(phase => phase[field]);
    values[phaseIndex] = value;

    switch (field) {
      case 'voltage':
        await setVoltage(values as [number, number, number]);
        meterData.voltage = values as [number, number, number];
        break;
      case 'current':
        await setCurrent(values as [number, number, number]);
        meterData.current = values as [number, number, number];
        break;
      case 'power':
        await setPower(values as [number, number, number]);
        meterData.power = values as [number, number, number];
        break;
    }
  }

  async function handleSerialNumberChange(event: Event) {
    const input = event.target as HTMLInputElement;
    const value = input.value;
    
    if (value.length <= 7 && /^\d*$/.test(value)) {
      await setSerialNumber(value);
      meterData.serialNumber = value;
    }
  }

  async function handleBrandChange(event: Event) {
    const select = event.target as HTMLSelectElement;
    const value = select.value as 'Brand1' | 'Brand2';
    await setBrand(value);
    meterData.brand = value;
  }
</script>

<main class="min-h-screen bg-gray-100 py-8 px-4">
  <div class="max-w-6xl mx-auto">
    <h1 class="text-3xl font-bold text-gray-900 mb-8">Power Meter Simulation</h1>
    
    <div class="mb-8 space-y-4">
      <div class="flex gap-4 items-end">
        <div class="flex-1">
          <label for="serialNumber" class="block text-sm font-medium text-gray-700">
            Serial Number (7 digits)
          </label>
          <input
            id="serialNumber"
            type="text"
            maxlength="7"
            pattern="\d*"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            value={meterData.serialNumber}
            on:input={handleSerialNumberChange}
          />
        </div>
        
        <div class="flex-1">
          <label for="brand" class="block text-sm font-medium text-gray-700">
            Brand
          </label>
          <select
            id="brand"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            value={meterData.brand}
            on:change={handleBrandChange}
          >
            <option value="Brand1">Brand 1</option>
            <option value="Brand2">Brand 2</option>
          </select>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      {#each phases as phase, i}
        <PhaseCard
          {phase}
          phaseNumber={i + 1}
          onUpdate={(field, value) => handlePhaseUpdate(i, field, value)}
        />
      {/each}
      }
    </div>
  </div>
</main>

<style>
  :global(body) {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  }
</style>