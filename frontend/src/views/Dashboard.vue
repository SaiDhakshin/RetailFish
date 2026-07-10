<template>
  <div class="dashboard">
    <SearchBox
      @selected="loadCandles"
    />

    <TradingChart
      :candles="candles"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

import SearchBox from "@/components/SearchBox.vue";
import TradingChart from "@/components/TradingChart.vue";

import { getCandles } from "@/services/candle.service";

import type { Candle } from "@/types/candle";
import type { Instrument } from "@/types/instrument";

const candles = ref<Candle[]>([]);

async function loadCandles(
  instrument: Instrument,
) {
  candles.value =
    await getCandles(instrument.symbol);

    console.log(instrument.symbol,candles.value.length,);
}
</script>

<style scoped>
.dashboard {
  padding: 24px;
}
</style>