<template>
  <div
    ref="container"
    class="search-box"
  >
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

    <div
      v-if="loading"
      class="loading"
    >
      Searching...
    </div>

    <ul
      v-if="showDropdown && results.length"
      class="dropdown"
    >
      <li
        v-for="(instrument, index) in results"
        :key="instrument.id"
        :class="{
          active: highlightedIndex === index,
        }"
        @mousedown.prevent="selectInstrument(instrument)"
      >
        {{ instrument.symbol }}
      </li>
    </ul>

    <div
      v-if="
        showDropdown &&
        !loading &&
        query.length > 0 &&
        results.length === 0
      "
      class="empty"
    >
      No matching instruments
    </div>
  </div>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, watch } from "vue";

import { searchInstruments } from "@/services/instrument.service";
import type { Instrument } from "@/types/instrument";

const emit = defineEmits<{
  (e: "selected", instrument: Instrument): void;
}>();

const query = ref("");

const loading = ref(false);

const results = ref<Instrument[]>([]);

const highlightedIndex = ref(-1);

const showDropdown = ref(false);

const container = ref<HTMLElement | null>(null);

let debounceTimer: number | undefined;

watch(query, (value) => {
  window.clearTimeout(debounceTimer);

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

    results.value = response.items;

    highlightedIndex.value =
      response.items.length > 0 ? 0 : -1;

    showDropdown.value = true;
  } catch (error) {
    console.error(error);

    results.value = [];
  } finally {
    loading.value = false;
  }
}

function selectInstrument(
  instrument: Instrument,
) {
  query.value = instrument.symbol;

  showDropdown.value = false;

  emit("selected", instrument);
}

function moveDown() {
  if (!showDropdown.value) return;

  if (
    highlightedIndex.value <
    results.value.length - 1
  ) {
    highlightedIndex.value++;
  }
}

function moveUp() {
  if (!showDropdown.value) return;

  if (highlightedIndex.value > 0) {
    highlightedIndex.value--;
  }
}

function selectHighlighted() {
  if (
    highlightedIndex.value < 0 ||
    highlightedIndex.value >=
      results.value.length
  ) {
    return;
  }

  selectInstrument(
    results.value[highlightedIndex.value],
  );
}

function closeDropdown() {
  showDropdown.value = false;
}

function handleClickOutside(
  event: MouseEvent,
) {
  if (
    container.value &&
    !container.value.contains(
      event.target as Node,
    )
  ) {
    showDropdown.value = false;
  }
}

onMounted(() => {
  document.addEventListener(
    "click",
    handleClickOutside,
  );
});

onBeforeUnmount(() => {
  document.removeEventListener(
    "click",
    handleClickOutside,
  );
});
</script>

<style scoped>
.search-box {
  position: relative;
  width: 400px;
}

.search-input {
  width: 100%;
  padding: 10px;
  font-size: 15px;
}

.loading {
  margin-top: 8px;
  font-size: 14px;
}

.dropdown {
  position: absolute;
  z-index: 1000;
  width: 100%;
  max-height: 320px;
  margin: 4px 0 0;
  padding: 0;
  list-style: none;
  overflow-y: auto;
  background: white;
  border: 1px solid #ddd;
}

.dropdown li {
  padding: 10px;
  cursor: pointer;
}

.dropdown li:hover,
.dropdown li.active {
  background: #f5f5f5;
}

.empty {
  margin-top: 8px;
  padding: 10px;
  border: 1px solid #ddd;
}
</style>