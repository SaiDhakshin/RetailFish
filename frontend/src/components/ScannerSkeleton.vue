<template>
  <div class="symbols">
    <div v-for="i in 8" :key="i" class="symbol-skeleton">
      <div class="top-row">
        <div class="ticker-skeleton skeleton"></div>
        <div class="price-skeleton skeleton"></div>
      </div>
      <div class="bottom-row">
        <div class="badge-skeleton skeleton"></div>
        <div class="badge-skeleton skeleton"></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.symbols {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  margin: 0.5rem 0;
}

.symbol-skeleton {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid transparent;
  border-radius: 4px;
  background: transparent;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.top-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
}

.ticker-skeleton {
  width: 60px;
  height: 16px;
}

.price-skeleton {
  width: 80px;
  height: 16px;
}

.bottom-row {
  display: flex;
  gap: 6px;
  align-items: center;
}

.badge-skeleton {
  width: 40px;
  height: 14px;
  border-radius: 2px;
}

.skeleton {
  background: linear-gradient(
    90deg,
    rgba(52, 199, 89, 0.1) 0%,
    rgba(52, 199, 89, 0.2) 50%,
    rgba(52, 199, 89, 0.1) 100%
  );
  background-size: 200% 100%;
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}
</style>
