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
            <div class="quote-controls">
              <label>
                Quote Mode
                <select v-model="quoteMode">
                  <option value="manual">Manual</option>
                  <option value="polling">Polling</option>
                  <option value="realtime" disabled>
                    Realtime (Coming Soon)
                  </option>
                </select>
              </label>
              <button type="button" @click="refreshQuotes">Refresh</button>
            </div>
            <button
              :disabled="!selectedSymbol"
              @click="showDialog = true"
              class="add-btn"
            >
              Add to Watchlist
            </button>
          </div>

          <TradingChart
            :candles="candles"
            :overlays="scannerResult?.overlays ?? []"
          />
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
import { useQuoteStore, type QuoteMode } from "@/stores/quote";
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
const quoteStore = useQuoteStore();

const scannerResult = computed(() => scannerStore.selectedResult);

const candles = ref<Candle[]>([]);

const selectedTimeframe = ref<TimeFrame>("1d");

const selectedSymbol = ref<string | null>(null);

const quoteMode = computed<QuoteMode>({
  get: () => quoteStore.mode,
  set: (value) => void quoteStore.setQuoteMode(value),
});

const showDialog = ref(false);

async function loadCandles(symbol: string) {
  selectedSymbol.value = symbol;
  scannerStore.selectSymbol(symbol);

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

function refreshQuotes() {
  void quoteStore.refreshActiveSymbols();
}
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

.quote-controls {
  display: flex;
  align-items: center;
  gap: 10px;
}

.quote-controls label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--text);
}

.quote-controls select,
.quote-controls button {
  height: 28px;
  border: 1px solid var(--border);
  background: transparent;
  color: var(--text);
  border-radius: 4px;
  font-family: var(--mono);
  font-size: 12px;
  padding: 0 8px;
  cursor: pointer;
}

.quote-controls button:hover {
  background: rgba(52, 199, 89, 0.08);
  border-color: var(--accent);
  color: var(--accent);
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
