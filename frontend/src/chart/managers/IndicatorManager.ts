import type { IChartApi } from "lightweight-charts";

import type { Candle } from "@/types/candle";
import type { IndicatorConfig, IndicatorType } from "@/types/indicator";

import type { Indicator } from "../Indicator";

export class IndicatorManager {
  private readonly chart: IChartApi;

  private readonly indicators = new Map<IndicatorType, Indicator>();

  constructor(chart: IChartApi) {
    this.chart = chart;
  }

  register(indicator: Indicator): void {
    console.log("IndicatorManager.register", indicator.type);
    if (this.indicators.has(indicator.type)) {
      throw new Error(`Indicator '${indicator.type}' already exists.`);
    }

    indicator.create(this.chart);

    this.indicators.set(indicator.type, indicator);
  }

  unregister(type: IndicatorType): void {
    const indicator = this.indicators.get(type);

    if (!indicator) {
      return;
    }

    indicator.destroy();

    this.indicators.delete(type);
  }

  update(candles: Candle[]): void {
    for (const indicator of this.indicators.values()) {
      indicator.update(candles);
    }
  }

  applyConfig(configs: Record<IndicatorType, IndicatorConfig>): void {
    for (const [type, indicator] of this.indicators) {
      indicator.applyConfig(configs[type]);
    }
  }

  destroy(): void {
    for (const indicator of this.indicators.values()) {
      indicator.destroy();
    }

    this.indicators.clear();
  }
}
