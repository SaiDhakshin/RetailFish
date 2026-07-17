import {
  createSeriesMarkers,
  LineSeries,
  type IChartApi,
  type ISeriesApi,
  type SeriesMarkerPrice,
  type SeriesMarkerShape,
  type UTCTimestamp,
} from "lightweight-charts";

import type { ChartOverlay } from "@/types/overlay";

const markerShapeMap: Record<string, SeriesMarkerShape> = {
  label: "circle",
  marker: "circle",
  horizontalLine: "square",
  polyline: "circle",
};

export class OverlayManager {
  private readonly chart: IChartApi;

  private readonly markerSeries: ISeriesApi<"Line">;

  private readonly lineSeries = new Map<string, ISeriesApi<"Line">>();

  private readonly seriesMarkers = new Map<
    string,
    ReturnType<typeof createSeriesMarkers>
  >();

  constructor(chart: IChartApi) {
    this.chart = chart;
    this.markerSeries = chart.addSeries(LineSeries, {
      color: "rgba(0, 0, 0, 0)",
      lineWidth: 1,
      visible: false,
    });
  }

  public setOverlays(overlays: ChartOverlay[]): void {
    this.clear();

    if (!overlays || overlays.length === 0) {
      return;
    }

    const markers: SeriesMarkerPrice<UTCTimestamp>[] = [];

    for (const overlay of overlays) {
      const seriesData = overlay.points.map((point) => {
        return {
          time: this.normalizeTime(point.time),
          value: point.value,
        };
      });

      if (overlay.type === "polyline" || overlay.type === "horizontalLine") {
        if (seriesData.length < 2) {
          continue;
        }

        const lineSeries = this.chart.addSeries(LineSeries, {
          color: overlay.color,
          lineWidth: overlay.type === "horizontalLine" ? 1 : 2,
          lineStyle: overlay.type === "horizontalLine" ? 2 : 0,
          visible: true,
          crosshairMarkerVisible: false,
          lastValueVisible: false,
          priceLineVisible: false,
        });

        lineSeries.setData(seriesData);
        this.lineSeries.set(overlay.id, lineSeries);
        continue;
      }

      for (const point of overlay.points) {
        markers.push({
          time: this.normalizeTime(point.time),
          position: overlay.type === "label" ? "atPriceTop" : "atPriceMiddle",
          shape: markerShapeMap[overlay.type] ?? "circle",
          color: overlay.color,
          text: overlay.text,
          price: point.value,
          size: 6,
        });
      }
    }

    if (markers.length > 0) {
      const markerApi = createSeriesMarkers(this.markerSeries, markers, {
        zOrder: "top",
      }) as ReturnType<typeof createSeriesMarkers>;
      this.seriesMarkers.set("overlay-markers", markerApi);
    }
  }

  public destroy(): void {
    this.clear();
  }

  private clear(): void {
    for (const markerApi of this.seriesMarkers.values()) {
      markerApi.setMarkers([]);
    }

    for (const series of this.lineSeries.values()) {
      this.chart.removeSeries(series);
    }

    this.seriesMarkers.clear();
    this.lineSeries.clear();
  }

  private normalizeTime(time: string | number | Date): UTCTimestamp {
    if (typeof time === "number") {
      return Math.floor(time) as UTCTimestamp;
    }

    if (typeof time === "string") {
      return Math.floor(new Date(time).getTime() / 1000) as UTCTimestamp;
    }

    return Math.floor(time.getTime() / 1000) as UTCTimestamp;
  }
}
