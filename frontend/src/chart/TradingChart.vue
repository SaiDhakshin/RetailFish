<template>
  <div class="chart-wrapper">
    <div ref="chartContainer" class="chart-container" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch, nextTick } from "vue";

import { ChartEngine } from "@/chart/ChartEngine";

import { useChartStore } from "@/stores/chart";

import { useIndicatorStore } from "@/stores/indicator";

import { createIndicators } from "@/chart/createIndicators";

import type { Candle } from "@/types/candle";

const props = defineProps<{
  candles: Candle[];
  overlays?: import("@/types/overlay").ChartOverlay[];
}>();

const chartContainer = ref<HTMLDivElement | null>(null);

const indicatorStore = useIndicatorStore();

const chartStore = useChartStore();

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

  engine.setVolumeVisible(chartStore.showVolume);

  engine.setCandles(props.candles);
  engine.setOverlays(props.overlays ?? []);
});

function resetZoom() {
  engine?.resetZoom();
}

watch(
  () => props.candles,

  (candles) => {
    engine?.setCandles(candles);
    engine?.setOverlays(props.overlays ?? []);
    nextTick(() => {
      if (chartContainer.value && engine) {
        const width = chartContainer.value.clientWidth;
        const height = chartContainer.value.clientHeight;
        if (width > 0 && height > 0) {
          engine.resize(width, height);
        }
      }
    });
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

watch(
  () => props.overlays,
  (overlays) => {
    engine?.setOverlays(overlays ?? []);
  },
  {
    deep: true,
  },
);

watch(
  () => chartStore.showVolume,
  (visible) => {
    engine?.setVolumeVisible(visible);
  },
);

defineExpose({
  resetZoom,
});

onBeforeUnmount(() => {
  engine?.destroy();
});
</script>

<style scoped>
.chart-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  min-height: 400px;
}

.chart-container {
  width: 100%;
  height: 100%;
  flex: 1;
}
</style>
