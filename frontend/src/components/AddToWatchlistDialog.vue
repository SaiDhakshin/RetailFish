<script setup lang="ts">
import { computed, ref } from "vue";

import { useWatchlistStore } from "@/stores/watchlist";

const props = defineProps<{
  symbol: string;
  open: boolean;
}>();

const emit = defineEmits<{
  (e: "close"): void;
}>();

const store = useWatchlistStore();

const selected = ref<number>();

const watchlists = computed(() => store.watchlists);

async function add() {
  if (!selected.value) {
    return;
  }

  await store.addSymbol(selected.value, props.symbol);

  emit("close");
}
</script>

<template>
  <div v-if="open" class="overlay">
    <div class="dialog">
      <h3>Add to Watchlist</h3>

      <p>{{ symbol }}</p>

      <select v-model="selected">
        <option disabled :value="undefined">Select Watchlist</option>

        <option
          v-for="watchlist in watchlists"
          :key="watchlist.id"
          :value="watchlist.id"
        >
          {{ watchlist.name }}
        </option>
      </select>

      <div class="actions">
        <button @click="emit('close')">Cancel</button>

        <button @click="add">Add</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  backdrop-filter: blur(2px);
}

.dialog {
  z-index: 10000;
  background: var(--bg);
  padding: 20px;
  border: 1px solid var(--border);
  border-radius: 4px;
  width: 320px;
  box-shadow: var(--shadow);
}

.dialog h3 {
  font-size: 16px;
  color: var(--text-h);
  margin: 0 0 12px;
  font-family: var(--heading);
  font-weight: 600;
}

.dialog p {
  font-size: 13px;
  color: var(--accent);
  font-family: var(--mono);
  font-weight: 600;
  margin: 0 0 12px;
}

select {
  width: 100%;
  padding: 8px 10px;
  font-size: 13px;
  font-family: var(--mono);
  background: transparent;
  border: 1px solid var(--border);
  border-radius: 4px;
  color: var(--text);
  outline: none;
  transition: all 0.2s;
  margin-bottom: 12px;
}

select:focus {
  border-color: var(--accent);
}

select option {
  background: var(--code-bg);
  color: var(--text);
}

.actions {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

.actions button {
  padding: 8px 12px;
  font-size: 13px;
  font-family: var(--mono);
  border: 1px solid var(--border);
  border-radius: 4px;
  cursor: pointer;
  background: transparent;
  color: var(--text);
  transition: all 0.2s;
}

.actions button:first-child {
  border-color: var(--border);
  color: var(--secondary);
}

.actions button:first-child:hover {
  background: rgba(161, 161, 161, 0.1);
  border-color: var(--secondary);
}

.actions button:last-child {
  border-color: var(--accent);
  color: var(--accent);
}

.actions button:last-child:hover {
  background: rgba(52, 199, 89, 0.15);
}
</style>
