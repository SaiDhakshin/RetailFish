<script setup lang="ts">
import { computed, onMounted, onUnmounted } from "vue";

import { useWatchlistStore } from "@/stores/watchlist";

import type { Quote } from "@/types/quote";
import type { WatchlistItem } from "@/types/watchlist";

const emit = defineEmits<{
  (e: "selected", symbol: string): void;
}>();

const store = useWatchlistStore();

const watchlists = computed(() => store.watchlists);

const items = computed(() => store.items);

const quotes = computed(() => store.quotes);

const selectedWatchlist = computed(() => store.selectedWatchlist);

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

function selectSymbol(item: WatchlistItem) {
  store.selectSymbol(item.symbol);

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

const selectedSymbol = computed(() => store.selectedSymbol);
</script>

<template>
  <aside class="sidebar">
    <div class="header">
      <h2>Watchlists</h2>
    </div>

    <div class="watchlists">
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
        :key="item.id"
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

          <span v-if="quoteFor(item.symbol)" class="price">
            ₹{{ quoteFor(item.symbol)!.price.toFixed(2) }}
          </span>

          <span v-else class="loading"> Loading... </span>
        </div>

        <div class="bottom-row" :class="quoteClass(quoteFor(item.symbol))">
          <template v-if="quoteFor(item.symbol)">
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
</style>
