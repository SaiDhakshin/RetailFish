import { ColorType, createChart, type IChartApi } from "lightweight-charts";

import type { Candle } from "@/types/candle";
import type { Indicator } from "./Indicator";
import type { IndicatorConfig, IndicatorType } from "@/types/indicator";

import { CandleLayer } from "./layers/CandleLayer";
import { IndicatorManager } from "./managers/IndicatorManager";
import { VolumeLayer } from "./layers/VolumeLayer";

export class ChartEngine {
  private readonly container: HTMLElement;

  private readonly chart: IChartApi;

  private readonly candleLayer: CandleLayer;

  private readonly indicatorManager: IndicatorManager;

  private readonly volumeLayer: VolumeLayer;

  private candles: Candle[] = [];

  constructor(container: HTMLElement, indicators: Indicator[]) {
    this.container = container;

    console.log("Creating chart engine");

    this.chart = createChart(container, {
      width: container.clientWidth,
      height: 600,

      layout: {
        background: {
          type: ColorType.Solid,
          color: "#0a0a0b",
        },
        textColor: "#a1a1a1",
        fontFamily: "'Menlo', 'Monaco', 'Courier New', monospace",
      },

      grid: {
        vertLines: {
          color: "#1d1d1f",
        },
        horzLines: {
          color: "#1d1d1f",
        },
      },

      crosshair: {
        mode: 0,
        vertLine: {
          color: "#34c759",
          width: 1,
          style: 1,
        },
        horzLine: {
          color: "#34c759",
          width: 1,
          style: 1,
        },
      },

      rightPriceScale: {
        borderVisible: true,
        borderColor: "#1d1d1f",
        textColor: "#a1a1a1",
      },

      timeScale: {
        borderVisible: true,
        borderColor: "#1d1d1f",
        timeVisible: true,
        secondsVisible: false,
        textColor: "#a1a1a1",
      },
    });

    this.candleLayer = new CandleLayer(this.chart);

    this.indicatorManager = new IndicatorManager(this.chart);

    this.volumeLayer = new VolumeLayer(this.chart);

    this.registerIndicators(indicators);

    window.addEventListener("resize", this.handleResize);
  }

  private registerIndicators(indicators: Indicator[]): void {
    console.log("Indicators passed:", indicators);
    for (const indicator of indicators) {
      this.indicatorManager.register(indicator);
    }
  }

  public setCandles(candles: Candle[]): void {
    this.candles = candles;

    this.candleLayer.setData(candles);

    this.volumeLayer.setData(candles);

    this.indicatorManager.update(candles);

    this.chart.timeScale().fitContent();
  }

  public updateIndicatorConfigs(
    configs: Record<IndicatorType, IndicatorConfig>,
  ): void {
    this.indicatorManager.applyConfig(configs);

    this.indicatorManager.update(this.candles);
  }

  public resize(width: number, height: number): void {
    this.chart.resize(width, height);
  }

  private handleResize = () => {
    this.resize(this.container.clientWidth, 600);
  };

  public destroy(): void {
    window.removeEventListener("resize", this.handleResize);

    this.indicatorManager.destroy();

    this.chart.remove();
  }

  public setVolumeVisible(visible: boolean): void {
    this.volumeLayer.setVisible(visible);
  }
}
