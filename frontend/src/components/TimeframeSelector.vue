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
.timeframe-button {
  padding: 6px 12px;
  border: 1px solid #d1d5db;
  background-color: #ffffff;
  color: #1f2937;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s ease;
}

.timeframe-button:hover {
  background-color: #f3f4f6;
}

.timeframe-button.active {
  background-color: #2563eb;
  color: #ffffff;
  border-color: #2563eb;
}
</style>