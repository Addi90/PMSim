<script lang="ts">
  import type { Phase, Domain } from './types';
  
  export let phase: Phase;
  export let phaseNumber: number;
  export let selectedDomain: Domain;
  export let onUpdate: (value: number) => void;

  $: value = phase[selectedDomain];
  $: unit = selectedDomain === 'voltage' ? 'V' : selectedDomain === 'current' ? 'A' : 'W';
</script>

<div class="glass p-6 rounded-lg">
  <h2 class="text-xl font-bold mb-4 text-white">Phase {phaseNumber}</h2>
  
  <div class="space-y-4">
    <div>
      <label class="block text-sm font-medium text-gray-200">{selectedDomain.charAt(0).toUpperCase() + selectedDomain.slice(1)} ({unit})</label>
      <input
        type="number"
        class="mt-1 block w-full rounded-none bg-gray-800 border-gray-700 text-white shadow-sm focus:border-blue-500 focus:ring-blue-500"
        value={value}
        on:input={(e) => onUpdate(parseFloat(e.currentTarget.value))}
      />
    </div>
    
    <div class="grid grid-cols-3 gap-4">
      <div class="text-gray-200">
        <span class="block text-sm">Voltage</span>
        <span class="text-lg">{phase.voltage}V</span>
      </div>
      <div class="text-gray-200">
        <span class="block text-sm">Current</span>
        <span class="text-lg">{phase.current}A</span>
      </div>
      <div class="text-gray-200">
        <span class="block text-sm">Power</span>
        <span class="text-lg">{phase.power}W</span>
      </div>
    </div>
  </div>
</div>