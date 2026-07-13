import { defineStore } from "pinia";

import type { IndicatorConfig, IndicatorType } from "@/types/indicator";
import type { LineWidth } from "lightweight-charts";

export interface IndicatorState {
  indicators: Record<IndicatorType, IndicatorConfig>;
}

export const useIndicatorStore = defineStore("indicator", {
  state: (): IndicatorState => ({
    indicators: {
      ema20: {
        type: "ema20",
        enabled: true,
        style: {
          color: "#34c759",
          lineWidth: 1,
        },
      },

      ema50: {
        type: "ema50",
        enabled: true,
        style: {
          color: "#ff9500",
          lineWidth: 1,
        },
      },

      ema200: {
        type: "ema200",
        enabled: true,
        style: {
          color: "#5a5a5e",
          lineWidth: 1,
        },
      },
      sma20: {
        type: "sma20",
        enabled: false,
        style: {
          color: "#34c759",
          lineWidth: 1,
        },
      },

      sma50: {
        type: "sma50",
        enabled: false,
        style: {
          color: "#ff9500",
          lineWidth: 1,
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
