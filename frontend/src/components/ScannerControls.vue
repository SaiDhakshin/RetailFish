<script setup lang="ts">
import { ref } from "vue";

import { ScanUniverse, ScanFilter } from "@/types/scanner";

const emit = defineEmits<{
  (
    e: "scan",
    payload: {
      universe: ScanUniverse;
      filters: ScanFilter[];
    },
  ): void;
}>();

const universe = ref<ScanUniverse>(ScanUniverse.NIFTY500);

const filters = ref<ScanFilter[]>([ScanFilter.EMA_ALIGNMENT]);

function toggleFilter(filter: ScanFilter) {
  const index = filters.value.indexOf(filter);

  if (index === -1) {
    filters.value.push(filter);
  } else {
    filters.value.splice(index, 1);
  }
}

function runScan() {
  emit("scan", {
    universe: universe.value,
    filters: filters.value,
  });
}

// Expose runScan method for keyboard shortcuts and parent component calls
defineExpose({
  runScan,
});
</script>

<template>
  <div class="scanner-controls">
    <label>Universe</label>

    <select v-model="universe">
      <option :value="ScanUniverse.NIFTY50">Nifty 50</option>

      <option :value="ScanUniverse.NIFTY100">Nifty 100</option>

      <option :value="ScanUniverse.NIFTY200">Nifty 200</option>

      <option :value="ScanUniverse.NIFTY500">Nifty 500</option>

      <option :value="ScanUniverse.ALL">All</option>
    </select>

    <label>Filters</label>

    <label>
      <input
        type="checkbox"
        :checked="filters.includes(ScanFilter.EMA_ALIGNMENT)"
        @change="toggleFilter(ScanFilter.EMA_ALIGNMENT)"
      />

      EMA Alignment
    </label>

    <label>
      <input
        type="checkbox"
        :checked="filters.includes(ScanFilter.VOLUME_BREAKOUT)"
        @change="toggleFilter(ScanFilter.VOLUME_BREAKOUT)"
      />

      Volume Breakout
    </label>

    <label>
      <input
        type="checkbox"
        :checked="filters.includes(ScanFilter.FIFTY_TWO_WEEK_HIGH)"
        @change="toggleFilter(ScanFilter.FIFTY_TWO_WEEK_HIGH)"
      />

      52 Week High
    </label>

    <label>
      <input
        type="checkbox"
        :checked="filters.includes(ScanFilter.RELATIVE_STRENGTH)"
        @change="toggleFilter(ScanFilter.RELATIVE_STRENGTH)"
      />

      Relative Strength
    </label>

    <label>
      <input
        type="checkbox"
        :checked="filters.includes(ScanFilter.CUP_HANDLE)"
        @change="toggleFilter(ScanFilter.CUP_HANDLE)"
      />

      Cup & Handle
    </label>

    <label>
      <input
        type="checkbox"
        :checked="filters.includes(ScanFilter.VCP)"
        @change="toggleFilter(ScanFilter.VCP)"
      />

      VCP
    </label>

    <button @click="runScan">Run Scan</button>
  </div>
</template>

<style scoped>
.scanner-controls {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 12px;
  margin-bottom: 12px;
}

label {
  font-size: 12px;
  color: var(--secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-family: var(--mono);
  font-weight: 600;
  margin-top: 8px;
}

label:first-child {
  margin-top: 0;
}

select {
  padding: 8px 10px;
  font-size: 13px;
  font-family: var(--mono);
  background: transparent;
  border: 1px solid var(--border);
  border-radius: 4px;
  color: var(--text);
  outline: none;
  transition: all 0.2s;
}

select:focus {
  border-color: var(--accent);
}

select option {
  background: var(--code-bg);
  color: var(--text);
}

input[type="checkbox"] {
  accent-color: var(--accent);
  cursor: pointer;
  margin-right: 6px;
}

label:has(input[type="checkbox"]) {
  display: flex;
  align-items: center;
  margin-top: 6px;
  margin-bottom: 0;
  text-transform: none;
  font-weight: 400;
  color: var(--text);
}

button {
  padding: 8px 12px;
  font-size: 13px;
  font-family: var(--mono);
  border: 1px solid var(--accent);
  cursor: pointer;
  background: transparent;
  color: var(--accent);
  border-radius: 4px;
  transition: all 0.2s;
  margin-top: 8px;
}

button:hover {
  background: rgba(52, 199, 89, 0.15);
}
</style>
