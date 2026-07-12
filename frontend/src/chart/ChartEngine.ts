import { ColorType, createChart, type IChartApi } from "lightweight-charts";

export class ChartEngine {
  private chart: IChartApi;

  constructor(container: HTMLElement) {
    this.chart = createChart(container, {
      width: container.clientWidth,

      height: 600,

      layout: {
        background: {
          type: ColorType.Solid,
          color: "#ffffff",
        },

        textColor: "#333333",
      },

      grid: {
        vertLines: {
          color: "#f0f0f0",
        },

        horzLines: {
          color: "#f0f0f0",
        },
      },

      crosshair: {
        mode: 0,
      },

      rightPriceScale: {
        borderVisible: false,
      },

      timeScale: {
        borderVisible: false,
        timeVisible: true,
      },
    });
  }

  get instance(): IChartApi {
    return this.chart;
  }

  resize(width: number, height: number) {
    this.chart.resize(width, height);
  }

  fitContent() {
    this.chart.timeScale().fitContent();
  }

  destroy() {
    this.chart.remove();
  }
}
