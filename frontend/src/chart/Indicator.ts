import type { IChartApi } from "lightweight-charts";

import type { Candle } from "@/types/candle";
import type { IndicatorConfig, IndicatorType } from "@/types/indicator";

export interface Indicator {
  /**
   * Unique indicator identifier.
   * Example:
   * ema20
   * ema50
   * ema200
   */
  readonly type: IndicatorType;

  /**
   * Called once after registration.
   */
  create(chart: IChartApi): void;

  /**
   * Update indicator using latest candles.
   */
  update(candles: Candle[]): void;

  /**
   * Apply latest configuration.
   */
  applyConfig(config: IndicatorConfig): void;

  /**
   * Cleanup resources.
   */
  destroy(): void;
}
