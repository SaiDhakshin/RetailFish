<template>
  <div>
    <div ref="chartContainer" class="chart-container" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch } from "vue";

import { ChartEngine } from "@/chart/ChartEngine";

import { EMAIndicator } from "@/chart/indicators/EMAIndicator";

import { useIndicatorStore } from "@/stores/indicator";

import { createIndicators } from "@/chart/createIndicators";

import type { Candle } from "@/types/candle";

const props = defineProps<{
  candles: Candle[];
}>();

const chartContainer = ref<HTMLDivElement | null>(null);

const indicatorStore = useIndicatorStore();

let engine: ChartEngine | null = null;

onMounted(() => {
  console.log("TradingChart mounted");

  if (!chartContainer.value) {
    console.log("Container is null");
    return;
  }

  console.log("Creating engine");

  engine = new ChartEngine(
    chartContainer.value,
    createIndicators(indicatorStore.indicators),
  );

  console.log("Engine created");

  engine.setCandles(props.candles);
});

watch(
  () => props.candles,

  (candles) => {
    engine?.setCandles(candles);
  },

  {
    deep: true,
  },
);

watch(
  () => indicatorStore.indicators,

  (configs) => {
    engine?.updateIndicatorConfigs(configs);
  },

  {
    deep: true,
  },
);

onBeforeUnmount(() => {
  engine?.destroy();
});
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 600px;
}
</style>
