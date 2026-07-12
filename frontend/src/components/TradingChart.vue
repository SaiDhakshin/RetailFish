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

import { calculateEMA } from "@/services/indicators/ema";

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

let ema20Series: ISeriesApi<"Line"> | null = null;

let ema50Series: ISeriesApi<"Line"> | null = null;

let ema200Series: ISeriesApi<"Line"> | null = null;

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

  ema20Series = chart.addSeries(LineSeries, {
    color: indicatorStore.config("ema20").style.color,

    lineWidth: indicatorStore.config("ema20").style.lineWidth,
  });

  ema50Series = chart.addSeries(LineSeries, {
    color: indicatorStore.config("ema50").style.color,

    lineWidth: indicatorStore.config("ema50").style.lineWidth,
  });

  ema200Series = chart.addSeries(LineSeries, {
    color: indicatorStore.config("ema200").style.color,

    lineWidth: indicatorStore.config("ema200").style.lineWidth,
  });

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
  const ema20 = calculateEMA(props.candles, 20);

  const ema50 = calculateEMA(props.candles, 50);

  const ema200 = calculateEMA(props.candles, 200);

  ema20Series?.setData(indicatorStore.config("ema20").enabled ? ema20 : []);

  ema50Series?.setData(indicatorStore.config("ema50").enabled ? ema50 : []);

  ema200Series?.setData(indicatorStore.config("ema200").enabled ? ema200 : []);
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
