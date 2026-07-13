import {
  CandlestickSeries,
  type IChartApi,
  type ISeriesApi,
  type CandlestickData,
  type UTCTimestamp,
} from "lightweight-charts";

import type { Candle } from "@/types/candle";

export class CandleLayer {
  private readonly series: ISeriesApi<"Candlestick">;

  constructor(chart: IChartApi) {
    this.series = chart.addSeries(CandlestickSeries, {
      upColor: "#34c759",
      downColor: "#ff3b30",
      borderUpColor: "#34c759",
      borderDownColor: "#ff3b30",
      wickUpColor: "#34c759",
      wickDownColor: "#ff3b30",
    });
  }

  public setData(candles: Candle[]): void {
    this.series.setData(this.toChartData(candles));
  }

  public update(candle: Candle): void {
    this.series.update({
      time: Math.floor(
        new Date(candle.timestamp).getTime() / 1000,
      ) as UTCTimestamp,

      open: candle.open,
      high: candle.high,
      low: candle.low,
      close: candle.close,
    });
  }

  public clear(): void {
    this.series.setData([]);
  }

  private toChartData(candles: Candle[]): CandlestickData<UTCTimestamp>[] {
    return candles
      .map((candle) => ({
        time: Math.floor(
          new Date(candle.timestamp).getTime() / 1000,
        ) as UTCTimestamp,

        open: candle.open,
        high: candle.high,
        low: candle.low,
        close: candle.close,
      }))
      .sort((a, b) => Number(a.time) - Number(b.time));
  }
}
