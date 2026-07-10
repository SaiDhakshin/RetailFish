<template>
  <div class="dashboard">
    <TimeframeSelector
      v-model="selectedTimeframe"
    />

    <SearchBox
      @selected="loadCandles"
    />

    <TradingChart
      :candles="candles"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";

import SearchBox from "@/components/SearchBox.vue";
import TradingChart from "@/components/TradingChart.vue";
import TimeframeSelector from "@/components/TimeframeSelector.vue"

import { getCandles } from "@/services/candle.service";

import type { Candle } from "@/types/candle";
import type { Instrument } from "@/types/instrument";
import type { TimeFrame } from "@/types/timeframe";

const candles = ref<Candle[]>([]);
const selectedTimeframe = ref<TimeFrame>("1d");

const selectedInstrument = ref<Instrument | null>(null);

async function loadCandles(
  instrument: Instrument,
) {
  selectedInstrument.value = instrument;

  candles.value =
    await getCandles(instrument.symbol,selectedTimeframe.value,);

    console.log(instrument.symbol,candles.value.length,);
}


watch(
  selectedTimeframe,
  async () => {
    if (!selectedInstrument.value) {
      return;
    }

    candles.value =
      await getCandles(
        selectedInstrument.value.symbol,
        selectedTimeframe.value,
      );
  },
);
</script>

<style scoped>
.dashboard {
  padding: 24px;
}
</style>