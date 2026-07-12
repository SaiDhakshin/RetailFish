import type { IChartApi } from "lightweight-charts";

import type { Candle } from "@/types/candle";
import type { IndicatorConfig, IndicatorType } from "@/types/indicator";

export interface Indicator {
  /**
   * Unique indicator id
   * Example:
   * ema20
   * ema50
   * rsi
   */
  readonly type: IndicatorType;

  /**
   * Create chart series.
   * Called once.
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
   * Show / hide indicator.
   */
  setVisible(visible: boolean): void;

  /**
   * Cleanup.
   */
  destroy(): void;
}
