<script setup lang="ts">
import { useScannerStore } from "@/stores/scanner";

const scannerStore = useScannerStore();

const sortOptions = [
  {
    label: "Score",
    value: "score",
  },
  {
    label: "Relative Strength",
    value: "relative_strength",
  },
  {
    label: "Volume Ratio",
    value: "volume_ratio",
  },
  {
    label: "52 Week High Distance",
    value: "distance_from_high",
  },
  {
    label: "Symbol",
    value: "symbol",
  },
];

function toggleDirection() {
  scannerStore.sortDirection =
    scannerStore.sortDirection === "asc" ? "desc" : "asc";
}
</script>

<template>
  <div class="scanner-sort">
    <label>Sort By</label>

    <div class="controls">
      <select v-model="scannerStore.sortBy">
        <option
          v-for="option in sortOptions"
          :key="option.value"
          :value="option.value"
        >
          {{ option.label }}
        </option>
      </select>

      <button class="direction" @click="toggleDirection">
        {{ scannerStore.sortDirection === "asc" ? "↑" : "↓" }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.scanner-sort {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.8rem;
  color: #999;
}

.controls {
  display: flex;
  gap: 0.5rem;
}

select {
  flex: 1;
  padding: 0.5rem;
  background: #202020;
  color: white;
  border: 1px solid #333;
  border-radius: 6px;
}

.direction {
  width: 40px;
  border: 1px solid #333;
  border-radius: 6px;
  background: #202020;
  color: white;
  cursor: pointer;
}

.direction:hover {
  background: #2b2b2b;
}
</style>
