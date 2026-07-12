<template>
  <div class="indicator-toolbar">
    <label
      v-for="indicator in indicators"
      :key="indicator.type"
      class="indicator-item"
    >
      <input
        type="checkbox"
        :checked="indicator.enabled"
        @change="toggle(indicator.type)"
      />

      {{ labels[indicator.type] }}
    </label>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";

import { useIndicatorStore } from "@/stores/indicator";

const store = useIndicatorStore();

const indicators = computed(() => Object.values(store.indicators));

const labels = {
  ema20: "EMA 20",
  ema50: "EMA 50",
  ema200: "EMA 200",
};

function toggle(type: keyof typeof labels) {
  store.toggle(type);
}
</script>

<style scoped>
.indicator-toolbar {
  display: flex;
  gap: 1rem;
  padding: 10px;
  border-bottom: 1px solid #ddd;
  background: white;
}

.indicator-item {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  font-size: 14px;
}
</style>
