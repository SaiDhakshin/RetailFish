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
  gap: 12px;
  padding: 0;
  margin: 0;
  background: transparent;
  font-family: var(--mono);
  font-size: 12px;
  align-items: center;
  flex-shrink: 0;
}

.section {
  display: flex;
  gap: 12px;
  align-items: center;
}

.indicator-item {
  display: flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  font-size: 12px;
  color: var(--text);
  user-select: none;
  white-space: nowrap;
}

.indicator-item:hover {
  color: var(--accent);
}

.indicator-item input[type="checkbox"] {
  accent-color: var(--accent);
  cursor: pointer;
  width: 14px;
  height: 14px;
}

hr {
  border: none;
  border-left: 1px solid var(--border);
  margin: 0;
  height: 20px;
  flex-shrink: 0;
}
</style>
