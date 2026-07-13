<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from "vue";

import ScannerControls from "@/components/ScannerControls.vue";

import { useWatchlistStore } from "@/stores/watchlist";
import { useScannerStore } from "@/stores/scanner";

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

  return scannerStore.results.map((item) => ({
    symbol: item.symbol,
    score: item.score,
    matchedFilters: item.matched_filters,
  }));
});

const quotes = computed(() => store.quotes);

const selectedWatchlist = computed(() => store.selectedWatchlist);

const mode = ref<"watchlist" | "scanner">("watchlist");

let refreshTimer: number | undefined;

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

  if (scannerStore.results.length > 0) {
    scannerStore.selectSymbol(scannerStore.results[0].symbol);

    emit("selected", scannerStore.results[0].symbol);
  }
}

const selectedSymbol = computed(() => store.selectedSymbol);
</script>

<template>
  <aside class="sidebar">
    <div class="header">
      <h2>Watchlists</h2>
    </div>
    <button @click="showScanner">Scanner</button>

    <button @click="showWatchlists">Watchlists</button>

    <ScannerControls v-if="mode === 'scanner'" @scan="runScan" />

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

    <hr />

    <div class="symbols">
      <button
        v-for="item in items"
        :key="item.symbol"
        class="symbol"
        :class="{
          active: selectedSymbol === item.symbol,
        }"
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

        <div
          class="bottom-row"
          :class="mode === 'watchlist' ? quoteClass(quoteFor(item.symbol)) : ''"
        >
          <div v-if="mode === 'scanner'" class="badges">
            <span
              v-for="filter in item.matchedFilters"
              :key="filter"
              class="badge"
            >
              {{ badgeLabel(filter) }}
            </span>
          </div>

          <template v-else-if="quoteFor(item.symbol)">
            {{ quoteFor(item.symbol)!.change > 0 ? "+" : "" }}
            {{ quoteFor(item.symbol)!.change.toFixed(2) }}

            (

            {{ quoteFor(item.symbol)!.change_percent > 0 ? "+" : "" }}

            {{ quoteFor(item.symbol)!.change_percent.toFixed(2) }}%)
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
  background: #171717;
  border-right: 1px solid #2e2e2e;
}

.header {
  margin-bottom: 1rem;
}

.watchlists,
.symbols {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.watchlist,
.symbol {
  width: 100%;
  text-align: left;
  padding: 0.75rem;
  border: none;
  border-radius: 8px;
  background: transparent;
  color: inherit;
  cursor: pointer;
  transition: background 0.2s;
}

.watchlist:hover,
.symbol:hover {
  background: #252525;
}

.watchlist.active {
  background: #2563eb;
  color: white;
}

.top-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.bottom-row {
  margin-top: 0.35rem;
  font-size: 0.85rem;
}

.ticker {
  font-weight: 600;
}

.price {
  font-weight: 500;
}

.loading {
  color: #888;
  font-size: 0.8rem;
}

.positive {
  color: #22c55e;
}

.negative {
  color: #ef4444;
}

.neutral {
  color: #9ca3af;
}

hr {
  border: none;
  border-top: 1px solid #2f2f2f;
  margin: 1rem 0;
}

.symbol.active {
  background: #2563eb;
  color: white;
}

.symbol.active:hover {
  background: #1d4ed8;
}

.symbol.active .positive,
.symbol.active .negative,
.symbol.active .neutral,
.symbol.active .loading {
  color: inherit;
  opacity: 0.9;
}

.score {
  font-weight: 600;
  color: #22c55e;
}

.actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.add-button {
  width: 24px;
  height: 24px;

  border: none;

  border-radius: 50%;

  cursor: pointer;

  background: #2563eb;

  color: white;

  font-weight: bold;
}

.add-button:hover {
  background: #1d4ed8;
}

.badges {
  display: flex;
  gap: 0.35rem;
  margin-top: 0.35rem;
  flex-wrap: wrap;
}

.badge {
  background: #2f2f2f;
  color: #ddd;
  font-size: 0.7rem;
  padding: 2px 8px;
  border-radius: 999px;
}

.actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.added {
  color: #22c55e;
  font-weight: bold;
}

.add-button {
  width: 22px;
  height: 22px;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  background: #2563eb;
  color: white;
  font-weight: bold;
}

.add-button:hover {
  background: #1d4ed8;
}
</style>
