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

  background: rgba(0, 0, 0, 0.5);

  display: flex;
  justify-content: center;
  align-items: center;
}

.dialog {
  z-index: 10000;

  background: #222;
  padding: 20px;
  border-radius: 8px;
  width: 320px;
}

.actions {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
