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
  gap: 0.75rem;
  margin-bottom: 1rem;
}

select {
  padding: 0.4rem;
}

button {
  padding: 0.6rem;
  border: none;
  cursor: pointer;
  background: #2563eb;
  color: white;
  border-radius: 6px;
}
</style>
