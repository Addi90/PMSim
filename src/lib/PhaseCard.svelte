<script lang="ts">
  import type { Phase } from './types';
  
  export let phase: Phase;
  export let phaseNumber: number;
  export let onUpdate: (field: keyof Phase, value: number) => void;
</script>

<div class="bg-white p-6 rounded-lg shadow-md">
  <h2 class="text-xl font-bold mb-4">Phase {phaseNumber}</h2>
  
  <div class="space-y-4">
    <div>
      <label class="block text-sm font-medium text-gray-700">Voltage (V)</label>
      <input
        type="number"
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        value={phase.voltage}
        on:input={(e) => onUpdate('voltage', parseFloat(e.currentTarget.value))}
      />
    </div>
    
    <div>
      <label class="block text-sm font-medium text-gray-700">Current (A)</label>
      <input
        type="number"
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        value={phase.current}
        on:input={(e) => onUpdate('current', parseFloat(e.currentTarget.value))}
      />
    </div>
    
    <div>
      <label class="block text-sm font-medium text-gray-700">Power (W)</label>
      <input
        type="number"
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        value={phase.power}
        on:input={(e) => onUpdate('power', parseFloat(e.currentTarget.value))}
      />
    </div>
  </div>
</div>