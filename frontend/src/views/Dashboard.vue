<template>
  <div class="dashboard">
    <SplitPane
      storage-key="dashboard-sidebar-width"
      :default-width="300"
      :min-width="240"
      :max-width="500"
    >
      <template #left>
        <WatchlistSidebar @selected="onSelected" />
      </template>

      <template #right>
        <div class="chart-container">
          <div class="toolbar-header">
            <TimeframeSelector v-model="selectedTimeframe" />
            <IndicatorToolbar />
            <SearchBox @selected="onSearchSelected" />
            <button :disabled="!selectedSymbol" @click="showDialog = true" class="add-btn">
              Add to Watchlist
            </button>
          </div>

          <TradingChart :candles="candles" />
          <ScannerDetails :result="scannerResult" />
        </div>
      </template>
    </SplitPane>
  </div>

  <AddToWatchlistDialog
    v-if="selectedSymbol"
    :symbol="selectedSymbol"
    :open="showDialog"
    @close="showDialog = false"
  />
</template>

<script setup lang="ts">
import { ref, watch, computed } from "vue";

import SplitPane from "@/components/layout/SplitPane.vue";
import IndicatorToolbar from "@/components/IndicatorToolbar.vue";

import SearchBox from "@/components/SearchBox.vue";
import TimeframeSelector from "@/components/TimeframeSelector.vue";
// import TradingChart from "@/components/TradingChart.vue";
import TradingChart from "@/chart/TradingChart.vue";
import WatchlistSidebar from "@/components/WatchlistSidebar.vue";
import AddToWatchlistDialog from "@/components/AddToWatchlistDialog.vue";
import ScannerDetails from "@/components/ScannerDetails.vue";

import { getCandles } from "@/services/candle.service";
import { useScannerStore } from "@/stores/scanner";

import type { Candle } from "@/types/candle";
import type { Instrument } from "@/types/instrument";
import type { TimeFrame } from "@/types/timeframe";

const scannerStore = useScannerStore();

const scannerResult = computed(() => scannerStore.selectedResult);

const candles = ref<Candle[]>([]);

const selectedTimeframe = ref<TimeFrame>("1d");

const selectedSymbol = ref<string | null>(null);

const showDialog = ref(false);

async function loadCandles(symbol: string) {
  selectedSymbol.value = symbol;

  candles.value = await getCandles(symbol, selectedTimeframe.value);

  console.log(symbol, candles.value.length);
}

async function onSearchSelected(instrument: Instrument) {
  await loadCandles(instrument.symbol);
}

async function onSelected(symbol: string) {
  await loadCandles(symbol);
}

watch(selectedTimeframe, async () => {
  if (!selectedSymbol.value) {
    return;
  }

  candles.value = await getCandles(
    selectedSymbol.value,
    selectedTimeframe.value,
  );
});
</script>

<style scoped>
.dashboard {
  width: 100%;
  height: 100%;
  background: var(--bg);
}

.chart-container {
  display: flex;
  flex-direction: column;
  gap: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: var(--bg);
}

.chart-container > :nth-child(3) {
  flex: 0 0 auto;
  overflow-y: auto;
  max-height: 200px;
  border-top: 1px solid var(--border);
}

.chart-container > :nth-child(2) {
  flex: 1;
  min-height: 400px;
  overflow: hidden;
}

.toolbar-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 1rem;
  border-bottom: 1px solid var(--border);
  background: var(--bg);
  flex-shrink: 0;
  min-height: 40px;
  max-height: 48px;
}

.add-btn {
  padding: 6px 12px;
  border: 1px solid var(--border);
  background: transparent;
  color: var(--text);
  border-radius: 4px;
  cursor: pointer;
  font-size: 13px;
  font-family: var(--mono);
  transition: all 0.2s;
  white-space: nowrap;
}

.add-btn:hover:not(:disabled) {
  background: rgba(52, 199, 89, 0.08);
  border-color: var(--accent);
  color: var(--accent);
}

.add-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
</style>
