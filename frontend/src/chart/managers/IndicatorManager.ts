import type { Candle } from "@/types/candle";
import type { IndicatorConfig, IndicatorType } from "@/types/indicator";

import type { Indicator } from "../Indicator";

export class IndicatorManager {
  private indicators = new Map<IndicatorType, Indicator>();

  /**
   * Register an indicator.
   */
  register(indicator: Indicator): void {
    this.indicators.set(indicator.type, indicator);
  }

  /**
   * Remove an indicator.
   */
  unregister(type: IndicatorType): void {
    const indicator = this.indicators.get(type);

    if (!indicator) {
      return;
    }

    indicator.destroy();

    this.indicators.delete(type);
  }

  /**
   * Update every indicator.
   */
  update(candles: Candle[]): void {
    for (const indicator of this.indicators.values()) {
      indicator.update(candles);
    }
  }

  /**
   * Apply new configuration.
   */
  applyConfig(type: IndicatorType, config: IndicatorConfig): void {
    const indicator = this.indicators.get(type);

    if (!indicator) {
      return;
    }

    indicator.applyConfig(config);

    indicator.setVisible(config.enabled);
  }

  /**
   * Remove everything.
   */
  destroy(): void {
    for (const indicator of this.indicators.values()) {
      indicator.destroy();
    }

    this.indicators.clear();
  }
}
