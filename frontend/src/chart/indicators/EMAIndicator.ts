import {
  LineSeries,
  type IChartApi,
  type ISeriesApi,
} from "lightweight-charts";

import { calculateEMA } from "@/services/calculations/ema";

import type { Candle } from "@/types/candle";
import type { IndicatorConfig, IndicatorType } from "@/types/indicator";

import type { Indicator } from "../Indicator";

export class EMAIndicator implements Indicator {
  public readonly type: IndicatorType;

  private readonly period: number;

  private config: IndicatorConfig;

  private chart: IChartApi | null = null;

  private series: ISeriesApi<"Line"> | null = null;

  constructor(type: IndicatorType, period: number, config: IndicatorConfig) {
    this.type = type;
    this.period = period;
    this.config = config;
  }

  create(chart: IChartApi): void {
    this.chart = chart;

    console.log("Creating", this.type);

    this.series = chart.addSeries(LineSeries, {
      color: this.config.style.color,
      lineWidth: this.config.style.lineWidth,
      visible: this.config.enabled,
      lastValueVisible: false,
      priceLineVisible: false,
    });
  }

  update(candles: Candle[]): void {
    if (!this.series) {
      return;
    }

    if (!this.config.enabled) {
      this.series.setData([]);
      return;
    }

    this.series.setData(calculateEMA(candles, this.period));
  }

  applyConfig(config: IndicatorConfig): void {
    this.config = config;

    if (!this.series) {
      return;
    }

    this.series.applyOptions({
      color: config.style.color,
      lineWidth: config.style.lineWidth,
      visible: config.enabled,
    });

    if (!config.enabled) {
      this.series.setData([]);
    }
  }

  destroy(): void {
    if (this.chart && this.series) {
      this.chart.removeSeries(this.series);
    }

    this.series = null;
    this.chart = null;
  }
}
