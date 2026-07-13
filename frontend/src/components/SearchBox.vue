<template>
  <div ref="container" class="search-box">
    <input
      v-model="query"
      class="search-input"
      type="text"
      placeholder="Search NSE stock..."
      autocomplete="off"
      @keydown.down.prevent="moveDown"
      @keydown.up.prevent="moveUp"
      @keydown.enter.prevent="selectHighlighted"
      @keydown.esc="closeDropdown"
    />

    <div v-if="loading" class="loading">Searching...</div>

    <ul v-if="showDropdown && results.length" class="dropdown">
      <li
        v-for="(result, index) in results"
        :key="result.id"
        :class="{
          active: highlightedIndex === index,
        }"
        @mousedown.prevent="selectInstrument(result)"
      >
        <div class="row">
          <div>
            <div class="symbol">
              {{ result.symbol }}
            </div>

            <div class="name">
              {{ result.name }}
            </div>
          </div>

          <div v-if="result.quote" class="quote">
            <div>₹{{ result.quote.price.toFixed(2) }}</div>

            <div
              :class="{
                positive: result.quote.change > 0,
                negative: result.quote.change < 0,
              }"
            >
              {{ result.quote.change_percent.toFixed(2) }}%
            </div>
          </div>
        </div>
      </li>
    </ul>

    <div
      v-if="
        showDropdown && !loading && query.length > 0 && results.length === 0
      "
      class="empty"
    >
      No matching instruments
    </div>
  </div>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, watch } from "vue";

import { getQuotes } from "@/services/quotes.service";
import { searchInstruments } from "@/services/instrument.service";

import type { Instrument } from "@/types/instrument";
import type { Quote } from "@/types/quote";

interface SearchResult extends Instrument {
  quote?: Quote;
}

const emit = defineEmits<{
  (e: "selected", instrument: Instrument): void;
}>();

const query = ref("");

const loading = ref(false);

const results = ref<SearchResult[]>([]);

const highlightedIndex = ref(-1);

const showDropdown = ref(false);

const container = ref<HTMLElement | null>(null);

let debounceTimer: number | undefined;

watch(query, (value) => {
  clearTimeout(debounceTimer);

  if (!value.trim()) {
    results.value = [];
    showDropdown.value = false;
    highlightedIndex.value = -1;
    return;
  }

  debounceTimer = window.setTimeout(async () => {
    await search(value);
  }, 300);
});

async function search(value: string) {
  try {
    loading.value = true;

    const response = await searchInstruments(value);

    const instruments = response.items;

    if (instruments.length === 0) {
      results.value = [];
      highlightedIndex.value = -1;
      showDropdown.value = true;
      return;
    }

    const quotes = await getQuotes(instruments.map((i) => i.symbol));

    const quoteMap = Object.fromEntries(
      quotes.map((quote) => [quote.symbol, quote]),
    );

    results.value = instruments.map((instrument) => ({
      ...instrument,
      quote: quoteMap[instrument.symbol],
    }));

    highlightedIndex.value = 0;
    showDropdown.value = true;
  } catch (error) {
    console.error(error);

    results.value = [];
  } finally {
    loading.value = false;
  }
}

function selectInstrument(instrument: Instrument) {
  query.value = instrument.symbol;

  showDropdown.value = false;

  emit("selected", instrument);
}

function moveDown() {
  if (!showDropdown.value) {
    return;
  }

  if (highlightedIndex.value < results.value.length - 1) {
    highlightedIndex.value++;
  }
}

function moveUp() {
  if (!showDropdown.value) {
    return;
  }

  if (highlightedIndex.value > 0) {
    highlightedIndex.value--;
  }
}

function selectHighlighted() {
  if (
    highlightedIndex.value < 0 ||
    highlightedIndex.value >= results.value.length
  ) {
    return;
  }

  selectInstrument(results.value[highlightedIndex.value]);
}

function closeDropdown() {
  showDropdown.value = false;
}

function handleClickOutside(event: MouseEvent) {
  if (container.value && !container.value.contains(event.target as Node)) {
    showDropdown.value = false;
  }
}

onMounted(() => {
  document.addEventListener("click", handleClickOutside);
});

onBeforeUnmount(() => {
  document.removeEventListener("click", handleClickOutside);
});
</script>

<style scoped>
.search-box {
  position: relative;
  width: 100%;
  max-width: 400px;
}

.search-input {
  width: 100%;
  padding: 8px 12px;
  font-size: 13px;
  font-family: var(--mono);
  background: transparent;
  border: 1px solid var(--border);
  border-radius: 4px;
  color: var(--text);
  outline: none;
  transition: all 0.2s;
}

.search-input:focus {
  border-color: var(--accent);
  background: rgba(52, 199, 89, 0.05);
}

.search-input::placeholder {
  color: var(--secondary);
}

.loading {
  margin-top: 8px;
  font-size: 12px;
  color: var(--secondary);
  padding: 8px 12px;
}

.dropdown {
  position: absolute;
  z-index: 1000;
  width: 100%;
  max-height: 350px;
  margin: 4px 0 0;
  padding: 0;
  list-style: none;
  overflow-y: auto;
  background: var(--code-bg);
  border: 1px solid var(--border);
  border-radius: 4px;
}

.dropdown li {
  padding: 10px 12px;
  cursor: pointer;
  transition: all 0.2s;
  border-bottom: 1px solid rgba(29, 29, 31, 0.5);
}

.dropdown li:last-child {
  border-bottom: none;
}

.dropdown li:hover {
  background: rgba(52, 199, 89, 0.1);
}

.dropdown li.active {
  background: rgba(52, 199, 89, 0.15);
  border-left: 2px solid var(--accent);
  padding-left: 10px;
}

.row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.symbol {
  font-weight: 600;
  color: var(--text-h);
}

.name {
  font-size: 12px;
  color: var(--secondary);
}

.quote {
  text-align: right;
  min-width: 80px;
  color: var(--accent);
}

.positive {
  color: var(--accent);
}

.negative {
  color: var(--danger);
}

.empty {
  margin-top: 8px;
  padding: 10px 12px;
  border: 1px solid var(--border);
  border-radius: 4px;
  color: var(--secondary);
  text-align: center;
}
</style>
