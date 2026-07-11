<script setup lang="ts">
import { ref } from "vue";

import { useWatchlistStore } from "@/stores/watchlist";

const props = defineProps<{
  open: boolean;
}>();

const emit = defineEmits<{
  (e: "close"): void;
}>();

const store = useWatchlistStore();

const name = ref("");

async function create() {
  if (!name.value.trim()) {
    return;
  }

  await store.createWatchlist(name.value.trim());

  name.value = "";

  emit("close");
}
</script>

<template>
  <div v-if="open" class="overlay">
    <div class="dialog">
      <h3>New Watchlist</h3>

      <input v-model="name" placeholder="Watchlist name" />

      <div class="actions">
        <button @click="emit('close')">Cancel</button>

        <button @click="create">Create</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: rgba(0, 0, 0, 0.4);

  display: flex;
  justify-content: center;
  align-items: center;
}

.dialog {
  background: #222;
  padding: 20px;
  border-radius: 8px;
  width: 320px;
}

.actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}
</style>
