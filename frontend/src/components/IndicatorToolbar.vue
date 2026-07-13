<template>
  <div class="indicator-toolbar">
    <div class="section">
      <label class="indicator-item">
        <input
          type="checkbox"
          :checked="chartStore.showVolume"
          @change="chartStore.toggleVolume()"
        />

        Volume
      </label>
    </div>

    <hr />
    <label
      v-for="indicator in indicators"
      :key="indicator.type"
      class="indicator-item"
    >
      <input
        type="checkbox"
        :checked="indicator.enabled"
        @change="toggle(indicator.type)"
      />

      {{ labels[indicator.type] }}
    </label>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";

import { useIndicatorStore } from "@/stores/indicator";

import { useChartStore } from "@/stores/chart";

const store = useIndicatorStore();

const chartStore = useChartStore();

const indicators = computed(() => Object.values(store.indicators));

const labels = {
  ema20: "EMA 20",
  ema50: "EMA 50",
  ema200: "EMA 200",
  sma20: "SMA 20",
  sma50: "SMA 50",
} as const;

function toggle(type: keyof typeof labels) {
  store.toggle(type);
}
</script>

<style scoped>
.indicator-toolbar {
  display: flex;
  gap: 1.5rem;
  padding: 12px 1rem;
  border-bottom: 1px solid var(--border);
  background: var(--bg);
  font-family: var(--mono);
  font-size: 13px;
}

.section {
  display: flex;
  gap: 1.5rem;
}

.indicator-item {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  font-size: 13px;
  color: var(--text);
  user-select: none;
}

.indicator-item:hover {
  color: var(--accent);
}

.indicator-item input[type="checkbox"] {
  accent-color: var(--accent);
  cursor: pointer;
  width: 16px;
  height: 16px;
}

hr {
  border: none;
  border-left: 1px solid var(--border);
  margin: 0 6px;
  height: auto;
}
</style>
