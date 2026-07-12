<template>
  <div ref="chartContainer" class="chart-container" />
</template>

<script setup lang="ts">
import {
  CandlestickSeries,
  LineSeries,
  ColorType,
  createChart,
  type IChartApi,
  type ISeriesApi,
} from "lightweight-charts";

import { onBeforeUnmount, onMounted, ref, watch } from "vue";

import { useIndicatorStore } from "@/stores/indicator";

import { calculateEMA } from "@/services/calculations/ema";

import type { Candle } from "@/types/candle";
import type {
  CandlestickData,
  LineData,
  UTCTimestamp,
} from "lightweight-charts";

const props = defineProps<{
  candles: Candle[];
}>();

const indicatorStore = useIndicatorStore();

const chartContainer = ref<HTMLDivElement | null>(null);

let chart: IChartApi | null = null;

let candleSeries: ISeriesApi<"Candlestick"> | null = null;

const emaConfigs = [
  {
    key: "ema20",
    period: 20,
  },
  {
    key: "ema50",
    period: 50,
  },
  {
    key: "ema200",
    period: 200,
  },
] as const;

const emaSeries: Record<
  (typeof emaConfigs)[number]["key"],
  ISeriesApi<"Line"> | null
> = {
  ema20: null,
  ema50: null,
  ema200: null,
};

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

  candleSeries = chart.addSeries(CandlestickSeries);

  const periods = [
    { key: "ema20", period: 20 },
    { key: "ema50", period: 50 },
    { key: "ema200", period: 200 },
  ] as const;

  for (const { key, period } of periods) {
    const data = calculateEMA(props.candles, period);

    emaSeries[key]?.setData(indicatorStore.config(key).enabled ? data : []);
  }

  updateChart();

  window.addEventListener("resize", resizeChart);
}

function toChartData(candles: Candle[]): CandlestickData<UTCTimestamp>[] {
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
  if (!chart || !candleSeries) return;

  candleSeries.setData(toChartData(props.candles));

  updateEMA();

  chart.timeScale().fitContent();
}

function updateEMA() {
  for (const config of emaConfigs) {
    const data = calculateEMA(props.candles, config.period);

    emaSeries[config.key]?.setData(
      indicatorStore.config(config.key).enabled ? data : [],
    );
  }
}

function resizeChart() {
  if (!chart || !chartContainer.value) return;

  chart.resize(chartContainer.value.clientWidth, 600);
}

watch(() => props.candles, updateChart);

watch(() => indicatorStore.indicators, updateEMA, {
  deep: true,
});

onMounted(renderChart);

onBeforeUnmount(() => {
  window.removeEventListener("resize", resizeChart);

  chart?.remove();
});
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 600px;
}
</style>
