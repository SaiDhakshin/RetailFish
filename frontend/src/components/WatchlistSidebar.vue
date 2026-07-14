<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref, nextTick } from "vue";

import ScannerControls from "@/components/ScannerControls.vue";
import ScannerSkeleton from "@/components/ScannerSkeleton.vue";
import ScannerSort from "@/components/ScannerSort.vue";

import { useWatchlistStore } from "@/stores/watchlist";
import { useScannerStore } from "@/stores/scanner";
import {
  useKeyboardShortcuts,
  scrollElementIntoView,
} from "@/composables/useKeyboardShortcuts";

import type { Quote } from "@/types/quote";
import type { ScanRequest } from "@/services/scanner.service";

import type { SidebarItem } from "@/types/sidebar";

const emit = defineEmits<{
  (e: "selected", symbol: string): void;
}>();

const store = useWatchlistStore();

const scannerStore = useScannerStore();

const watchlists = computed(() => store.watchlists);

const items = computed<SidebarItem[]>(() => {
  if (mode.value === "watchlist") {
    return store.items.map((item) => ({
      symbol: item.symbol,
      watchlistItemId: item.id,
    }));
  }

  return scannerStore.sortedResults.map((item) => ({
    symbol: item.symbol,
    score: item.score,
    matchedFilters: item.matched_filters,
    relativeStrength: item.relative_strength,
    volumeRatio: item.volume_ratio,
    distanceFromHigh: item.distance_from_high,
  }));
});

const quotes = computed(() => store.quotes);

const selectedWatchlist = computed(() => store.selectedWatchlist);

const mode = ref<"watchlist" | "scanner">("watchlist");

let refreshTimer: number | undefined;

const scannerControlsRef = ref<InstanceType<typeof ScannerControls> | null>(
  null,
);

onMounted(async () => {
  await store.loadWatchlists();

  if (items.value.length > 0) {
    store.selectSymbol(items.value[0].symbol);

    emit("selected", items.value[0].symbol);
  }

  refreshTimer = window.setInterval(async () => {
    await store.loadQuotes();
  }, 30000);
});

onUnmounted(() => {
  if (refreshTimer) {
    clearInterval(refreshTimer);
  }
});

async function selectWatchlist(id: number) {
  const watchlist = watchlists.value.find((w) => w.id === id);

  if (!watchlist) {
    return;
  }

  await store.selectWatchlist(watchlist);

  if (store.items.length > 0) {
    store.selectSymbol(store.items[0].symbol);

    emit("selected", store.items[0].symbol);
  }
}

function selectSymbol(item: SidebarItem) {
  if (mode.value === "watchlist") {
    store.selectSymbol(item.symbol);
  } else {
    scannerStore.selectSymbol(item.symbol);
  }

  emit("selected", item.symbol);
}

function quoteFor(symbol: string): Quote | undefined {
  return quotes.value[symbol];
}

function quoteClass(quote?: Quote): string {
  if (!quote) {
    return "";
  }

  if (quote.change > 0) {
    return "positive";
  }

  if (quote.change < 0) {
    return "negative";
  }

  return "neutral";
}

async function showScanner() {
  mode.value = "scanner";
}

function showWatchlists() {
  mode.value = "watchlist";

  if (store.items.length > 0) {
    store.selectSymbol(store.items[0].symbol);

    emit("selected", store.items[0].symbol);
  }
}

async function addToWatchlist(symbol: string) {
  if (!store.selectedWatchlist) {
    return;
  }

  await store.addSymbol(store.selectedWatchlist.id, symbol);
}

function isInWatchlist(symbol: string) {
  return store.items.some((item) => item.symbol === symbol);
}

function badgeLabel(filter: string) {
  switch (filter) {
    case "ema_alignment":
      return "EMA";

    case "volume_breakout":
      return "VOL";

    case "relative_strength":
      return "RS";

    case "fifty_two_week_high":
      return "52W";

    case "cup_handle":
      return "CUP";

    case "vcp":
      return "VCP";

    default:
      return filter;
  }
}

async function runScan(request: ScanRequest) {
  await scannerStore.scan(request);

  await store.loadQuotes(scannerStore.results.map((r) => r.symbol));

  if (scannerStore.results.length > 0) {
    scannerStore.selectSymbol(scannerStore.results[0].symbol);

    emit("selected", scannerStore.results[0].symbol);
  }
}

// Mode-aware selected symbol: use scanner store in scanner mode, watchlist store otherwise
const selectedSymbol = computed(() => {
  if (mode.value === "scanner") {
    return scannerStore.selectedSymbol;
  }
  return store.selectedSymbol;
});

const selectedIndex = computed(() => {
  const current = selectedSymbol.value;
  if (!current) return -1;
  return items.value.findIndex((item) => item.symbol === current);
});

function navigateNext(): void {
  const nextIndex = selectedIndex.value + 1;
  if (nextIndex < items.value.length) {
    const nextItem = items.value[nextIndex];
    selectSymbol(nextItem);
    scrollToSelected();
  }
}

function navigatePrevious(): void {
  const prevIndex = selectedIndex.value - 1;
  if (prevIndex >= 0) {
    const prevItem = items.value[prevIndex];
    selectSymbol(prevItem);
    scrollToSelected();
  }
}

function navigateFirst(): void {
  if (items.value.length > 0) {
    selectSymbol(items.value[0]);
    scrollToSelected();
  }
}

function navigateLast(): void {
  if (items.value.length > 0) {
    selectSymbol(items.value[items.value.length - 1]);
    scrollToSelected();
  }
}

function scrollToSelected(): void {
  nextTick(() => {
    const activeElement = document.querySelector(".sidebar .symbol.active");
    scrollElementIntoView(activeElement as HTMLElement | null);
  });
}

function handleAddToWatchlist(): void {
  if (
    mode.value === "scanner" &&
    selectedSymbol.value &&
    !isInWatchlist(selectedSymbol.value)
  ) {
    addToWatchlist(selectedSymbol.value);
  }
}

async function handleRemoveFromWatchlist(): void {
  if (mode.value === "watchlist" && selectedSymbol.value) {
    const item = store.items.find((i) => i.symbol === selectedSymbol.value);
    if (item && confirm(`Remove ${selectedSymbol.value} from watchlist?`)) {
      await store.removeSymbol(item.id);
    }
  }
}

// Initialize keyboard shortcuts
useKeyboardShortcuts({
  next: navigateNext,
  previous: navigatePrevious,
  first: navigateFirst,
  last: navigateLast,
  selectCurrent: () => {}, // Arrow keys already select
  runScanner: async () => {
    if (mode.value === "scanner" && scannerControlsRef.value) {
      // Call runScan() directly on ScannerControls component
      await scannerControlsRef.value.runScan();
    }
  },
  showScanner,
  showWatchlists,
  addToWatchlist: handleAddToWatchlist,
  removeFromWatchlist: handleRemoveFromWatchlist,
  closeDialog: () => {}, // Handled by parent
});
</script>

<template>
  <aside class="sidebar">
    <div class="header">
      <h2>Watchlists</h2>
    </div>
    <button @click="showScanner" title="Scanner (S)">Scanner</button>

    <button @click="showWatchlists" title="Watchlists (W)">Watchlists</button>

    <ScannerControls
      ref="scannerControlsRef"
      v-if="mode === 'scanner'"
      @scan="runScan"
    />

    <div v-if="mode === 'watchlist'" class="watchlists">
      <button
        v-for="watchlist in watchlists"
        :key="watchlist.id"
        class="watchlist"
        :class="{
          active: selectedWatchlist?.id === watchlist.id,
        }"
        @click="selectWatchlist(watchlist.id)"
      >
        {{ watchlist.name }}
      </button>
    </div>
    <ScannerSort v-if="mode === 'scanner'" />
    <hr />

    <ScannerSkeleton v-if="mode === 'scanner' && scannerStore.loading" />

    <div v-else class="symbols">
      <button
        v-for="item in items"
        :key="item.symbol"
        class="symbol"
        :class="{
          active: selectedSymbol === item.symbol,
        }"
        :title="`${item.symbol} (↑/↓ to navigate)`"
        @click="selectSymbol(item)"
      >
        <div class="top-row">
          <span class="ticker">
            {{ item.symbol }}
          </span>

          <div class="actions">
            <template v-if="mode === 'scanner'">
              <span class="score">
                {{ item.score }}
              </span>

              <button
                v-if="!isInWatchlist(item.symbol)"
                class="add-button"
                :title="`Add to Watchlist (A)`"
                @click.stop="addToWatchlist(item.symbol)"
              >
                +
              </button>

              <span v-else class="added"> ✓ </span>
            </template>

            <template v-else>
              <span v-if="quoteFor(item.symbol)" class="price">
                ₹{{ quoteFor(item.symbol)!.price.toFixed(2) }}
              </span>

              <span v-else class="loading"> Loading... </span>
            </template>
          </div>
        </div>

        <div class="bottom-row" :class="quoteClass(quoteFor(item.symbol))">
          <template v-if="quoteFor(item.symbol)">
            {{ quoteFor(item.symbol)!.change > 0 ? "+" : "" }}
            {{ quoteFor(item.symbol)!.change.toFixed(2) }}

            (

            {{ quoteFor(item.symbol)!.change_percent > 0 ? "+" : "" }}
            {{ quoteFor(item.symbol)!.change_percent.toFixed(2) }}%)

            <template v-if="mode === 'scanner'">
              • RS {{ item.relativeStrength?.toFixed(1) }}% • Vol
              {{ item.volumeRatio?.toFixed(1) }}× • 52W
              {{ item.distanceFromHigh?.toFixed(1) }}%
            </template>
          </template>

          <template v-else> -- </template>
        </div>
      </button>
    </div>
  </aside>
</template>

<style scoped>
.sidebar {
  height: 100%;
  overflow-y: auto;
  padding: 1rem;
  background: var(--bg);
  border-right: 1px solid var(--border);
  font-family: var(--mono);
}

.header {
  margin-bottom: 1rem;
}

.header h2 {
  font-size: 16px;
  color: var(--text-h);
  margin: 0;
  font-weight: 600;
}

button {
  width: 100%;
  text-align: left;
  padding: 8px 12px;
  border: 1px solid transparent;
  border-radius: 4px;
  background: transparent;
  color: var(--text);
  cursor: pointer;
  transition: all 0.2s;
  font-size: 13px;
  font-family: var(--mono);
  margin-bottom: 4px;
}

button:hover {
  background: rgba(52, 199, 89, 0.08);
  border-color: var(--border);
  color: var(--accent);
}

.watchlists,
.symbols {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  margin: 0.5rem 0;
}

.watchlist,
.symbol {
  width: 100%;
  text-align: left;
  padding: 8px 12px;
  border: 1px solid transparent;
  border-radius: 4px;
  background: transparent;
  color: var(--text);
  cursor: pointer;
  transition: all 0.2s;
  font-size: 13px;
  font-family: var(--mono);
}

.watchlist:hover,
.symbol:hover {
  background: rgba(52, 199, 89, 0.08);
  border-color: var(--border);
  color: var(--accent);
}

.watchlist.active {
  background: rgba(52, 199, 89, 0.15);
  border-color: var(--accent);
  color: var(--accent);
}

.symbol.active {
  background: rgba(52, 199, 89, 0.15);
  border-color: var(--accent);
  color: var(--accent);
}

.top-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.bottom-row {
  margin-top: 4px;
  font-size: 12px;
  color: var(--secondary);
}

.ticker {
  font-weight: 600;
  color: var(--text-h);
}

.price {
  font-weight: 500;
  color: var(--accent);
}

.loading {
  color: var(--secondary);
  font-size: 12px;
}

.positive {
  color: var(--accent);
}

.negative {
  color: var(--danger);
}

.neutral {
  color: var(--secondary);
}

hr {
  border: none;
  border-top: 1px solid var(--border);
  margin: 0.75rem 0;
}

.symbol.active .positive,
.symbol.active .negative,
.symbol.active .neutral,
.symbol.active .loading {
  color: inherit;
  opacity: 1;
}

.score {
  font-weight: 600;
  color: var(--accent);
}

.actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.add-button {
  width: 20px;
  height: 20px;
  border: 1px solid var(--accent);
  border-radius: 3px;
  cursor: pointer;
  background: transparent;
  color: var(--accent);
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.add-button:hover {
  background: rgba(52, 199, 89, 0.15);
}

.badges {
  display: flex;
  gap: 6px;
  margin-top: 4px;
  flex-wrap: wrap;
}

.badge {
  background: rgba(52, 199, 89, 0.1);
  color: var(--accent);
  font-size: 11px;
  padding: 3px 8px;
  border-radius: 2px;
  border: 1px solid rgba(52, 199, 89, 0.2);
}

.added {
  color: var(--accent);
  font-weight: bold;
}
</style>
