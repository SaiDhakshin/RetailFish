import { defineStore } from "pinia";

import type { IndicatorConfig, IndicatorType } from "@/types/indicator";
import type { LineWidth } from "lightweight-charts";

interface IndicatorState {
  indicators: Record<IndicatorType, IndicatorConfig>;
}

export const useIndicatorStore = defineStore("indicator", {
  state: (): IndicatorState => ({
    indicators: {
      ema20: {
        type: "ema20",
        enabled: true,
        style: {
          color: "#2962FF",
          lineWidth: 2,
        },
      },

      ema50: {
        type: "ema50",
        enabled: true,
        style: {
          color: "#FF9800",
          lineWidth: 2,
        },
      },

      ema200: {
        type: "ema200",
        enabled: true,
        style: {
          color: "#F44336",
          lineWidth: 2,
        },
      },
    },
  }),

  getters: {
    config: (state) => (indicator: IndicatorType) =>
      state.indicators[indicator],
  },

  actions: {
    toggle(indicator: IndicatorType) {
      this.indicators[indicator].enabled = !this.indicators[indicator].enabled;
    },

    setEnabled(indicator: IndicatorType, enabled: boolean) {
      this.indicators[indicator].enabled = enabled;
    },

    setColor(indicator: IndicatorType, color: string) {
      this.indicators[indicator].style.color = color;
    },

    setLineWidth(indicator: IndicatorType, width: LineWidth) {
      this.indicators[indicator].style.lineWidth = width;
    },
  },
});
