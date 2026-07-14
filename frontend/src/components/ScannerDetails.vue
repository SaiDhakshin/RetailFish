<template>
  <div class="scanner-details">
    <div v-if="!result" class="empty-state">
      <p>Select a scanner result to view details</p>
    </div>

    <div v-else class="details-content">
      <div class="header">
        <div class="symbol-score">
          <h3 class="symbol">{{ result.symbol }}</h3>
          <div class="score">{{ result.score }}</div>
        </div>
      </div>

      <div class="details-grid">
        <div v-for="(detail, filterKey) in result.details" :key="filterKey" class="detail-item">
          <div class="filter-name">{{ formatFilterName(filterKey) }}</div>
          <div class="filter-value">{{ detail.value }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ScannerResult } from "@/types/scanner";

defineProps<{
  result: ScannerResult | null;
}>();

function formatFilterName(filter: string): string {
  const names: Record<string, string> = {
    ema_alignment: "EMA Alignment",
    volume_breakout: "Volume Breakout",
    relative_strength: "Relative Strength",
    fifty_two_week_high: "52 Week High",
    cup_handle: "Cup Handle",
    vcp: "VCP",
    trend_template: "Trend Template",
  };
  return names[filter] || filter.replace(/_/g, " ");
}
</script>

<style scoped>
.scanner-details {
  padding: 16px;
  border-top: 1px solid var(--border);
  background: var(--bg);
  font-family: var(--mono);
  min-height: 120px;
}

.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 120px;
  color: var(--secondary);
  font-size: 13px;
  text-align: center;
}

.details-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.header {
  display: flex;
  align-items: center;
  gap: 16px;
  border-bottom: 1px solid var(--border);
  padding-bottom: 12px;
}

.symbol-score {
  display: flex;
  align-items: center;
  gap: 12px;
}

.symbol {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: var(--text-h);
  font-family: var(--heading);
}

.score {
  padding: 4px 12px;
  background: rgba(52, 199, 89, 0.1);
  border: 1px solid rgba(52, 199, 89, 0.3);
  border-radius: 4px;
  color: var(--accent);
  font-size: 14px;
  font-weight: 600;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 12px;
}

.detail-item {
  padding: 12px;
  background: rgba(29, 29, 31, 0.5);
  border: 1px solid var(--border);
  border-radius: 4px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.filter-name {
  font-size: 11px;
  color: var(--secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 600;
}

.filter-value {
  font-size: 13px;
  color: var(--text-h);
  font-weight: 500;
}

@media (max-width: 768px) {
  .details-grid {
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  }

  .scanner-details {
    padding: 12px;
  }
}
</style>
