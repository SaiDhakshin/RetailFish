<template>
  <div
    ref="chartContainer"
    class="chart-container"
  />
</template>

<script setup lang="ts">
import {
  CandlestickSeries,
  ColorType,
  createChart,
  type IChartApi,
  type ISeriesApi,
} from "lightweight-charts";

import {
  onBeforeUnmount,
  onMounted,
  ref,
  watch,
} from "vue";

import type { Candle } from "@/types/candle";
import type { UTCTimestamp, CandlestickData } from "lightweight-charts";

const props = defineProps<{
  candles: Candle[];
}>();

const chartContainer = ref<HTMLDivElement | null>(null);

let chart: IChartApi | null = null;

let candleSeries: ISeriesApi<"Candlestick"> | null =
  null;

function renderChart() {
  if (!chartContainer.value) return;

  chart = createChart(chartContainer.value, {
    width: chartContainer.value.clientWidth,
    height: 600,

    layout: {
      background: {
        type: ColorType.Solid,
        color: "#ffffff",
      },
      textColor: "#333",
    },

    grid: {
      vertLines: {
        color: "#f0f0f0",
      },
      horzLines: {
        color: "#f0f0f0",
      },
    },

    crosshair: {
      mode: 0,
    },

    rightPriceScale: {
      borderVisible: false,
    },

    timeScale: {
      borderVisible: false,
      timeVisible: true,
    },
  });

  candleSeries =
    chart.addSeries(CandlestickSeries);

  updateChart();

  window.addEventListener(
    "resize",
    resizeChart,
  );
}

function toChartData(
  candles: Candle[],
): CandlestickData<UTCTimestamp>[] {
  return candles
    .map((candle) => ({
      time: Math.floor(
        new Date(candle.timestamp).getTime() / 1000,
      ) as UTCTimestamp,

      open: candle.open,
      high: candle.high,
      low: candle.low,
      close: candle.close,
    }))
    .sort((a, b) => Number(a.time) - Number(b.time));
}

function updateChart() {
  if (!candleSeries) return;

  candleSeries.setData(
    toChartData(props.candles),
  );

  chart?.timeScale().fitContent();
}

function resizeChart() {
  if (!chart || !chartContainer.value) return;

  chart.resize(
    chartContainer.value.clientWidth,
    600,
  );
}

watch(
  () => props.candles,
  () => {
    updateChart();
  },
);

onMounted(() => {
  renderChart();
});

onBeforeUnmount(() => {
  window.removeEventListener(
    "resize",
    resizeChart,
  );

  chart?.remove();
});
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 600px;
}
</style>