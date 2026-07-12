export type IndicatorType = "ema20" | "ema50" | "ema200" | "sma20" | "sma50";
import type { LineWidth } from "lightweight-charts";

export interface IndicatorStyle {
  color: string;
  lineWidth: LineWidth;
}

export interface IndicatorConfig {
  type: IndicatorType;

  enabled: boolean;

  style: IndicatorStyle;
}
