import {
  HistogramSeries,
  type HistogramData,
  type IChartApi,
  type ISeriesApi,
  type UTCTimestamp,
} from "lightweight-charts";

import type { Candle } from "@/types/candle";

export class VolumeLayer {
  private readonly series: ISeriesApi<"Histogram">;

  constructor(chart: IChartApi) {
    this.series = chart.addSeries(HistogramSeries, {
      priceScaleId: "volume",

      priceFormat: {
        type: "volume",
      },

      lastValueVisible: false,

      priceLineVisible: false,
    });

    chart.priceScale("volume").applyOptions({
      scaleMargins: {
        top: 0.8,
        bottom: 0,
      },
    });
  }

  public setData(candles: Candle[]): void {
    this.series.setData(this.toData(candles));
  }

  public clear(): void {
    this.series.setData([]);
  }

  private toData(candles: Candle[]): HistogramData<UTCTimestamp>[] {
    return candles.map((candle) => ({
      time: Math.floor(
        new Date(candle.timestamp).getTime() / 1000,
      ) as UTCTimestamp,

      value: candle.volume,

      color: candle.close >= candle.open ? "#34c759" : "#ff3b30",
    }));
  }

  public setVisible(visible: boolean): void {
    this.series.applyOptions({
      visible,
    });
  }
}
