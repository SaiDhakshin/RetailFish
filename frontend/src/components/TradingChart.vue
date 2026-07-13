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
        color: "#0a0a0b",
      },
      textColor: "#a1a1a1",
      fontFamily: "'Menlo', 'Monaco', 'Courier New', monospace",
    },

    grid: {
      vertLines: {
        color: "#1d1d1f",
      },
      horzLines: {
        color: "#1d1d1f",
      },
    },

    crosshair: {
      mode: 0,
      vertLine: {
        color: "#34c759",
        width: 1,
        style: 1,
      },
      horzLine: {
        color: "#34c759",
        width: 1,
        style: 1,
      },
    },

    rightPriceScale: {
      borderVisible: true,
      borderColor: "#1d1d1f",
      textColor: "#a1a1a1",
    },

    timeScale: {
      borderVisible: true,
      borderColor: "#1d1d1f",
      timeVisible: true,
      secondsVisible: false,
      textColor: "#a1a1a1",
    },
  });

  candleSeries = chart.addSeries(CandlestickSeries, {
    upColor: "#34c759",
    downColor: "#ff3b30",
    borderUpColor: "#34c759",
    borderDownColor: "#ff3b30",
    wickUpColor: "#34c759",
    wickDownColor: "#ff3b30",
  });

  const periods = [
    { key: "ema20", period: 20, color: "#34c759" },
    { key: "ema50", period: 50, color: "#ff9500" },
    { key: "ema200", period: 200, color: "#5a5a5e" },
  ] as const;

  for (const { key, period, color } of periods) {
    const lineSeries = chart.addSeries(LineSeries, {
      color: color,
      lineWidth: 1,
    });
    emaSeries[key] = lineSeries;
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
