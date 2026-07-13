<template>
  <div class="timeframe-selector">
    <button
      v-for="item in TIMEFRAMES"
      :key="item.value"
      :class="[
        'timeframe-button',
        {
          active:
            modelValue === item.value,
        },
      ]"
      @click="$emit('update:modelValue', item.value)"
    >
      {{ item.label }}
    </button>
  </div>
</template>

<script setup lang="ts">
import {
  TIMEFRAMES,
  type TimeFrame,
} from "@/types/timeframe";

defineProps<{
  modelValue: TimeFrame;
}>();

defineEmits<{
  (
    e: "update:modelValue",
    value: TimeFrame,
  ): void;
}>();
</script>

<style scoped>
.timeframe-selector {
  display: flex;
  gap: 4px;
  padding: 0;
  margin: 0;
  align-items: center;
  flex-shrink: 0;
}

.timeframe-button {
  padding: 4px 8px;
  border: 1px solid var(--border);
  background-color: transparent;
  color: var(--text);
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  font-family: var(--mono);
  transition: all 0.2s ease;
  white-space: nowrap;
}

.timeframe-button:hover {
  background-color: rgba(52, 199, 89, 0.05);
  border-color: var(--accent);
  color: var(--accent);
}

.timeframe-button.active {
  background-color: rgba(52, 199, 89, 0.15);
  color: var(--accent);
  border-color: var(--accent);
}
</style>
