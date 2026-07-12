import { EMAIndicator } from "./indicators/EMAIndicator";
import { SMAIndicator } from "./indicators/SMAIndicator";

import type { Indicator } from "./Indicator";
import type { IndicatorState } from "@/stores/indicator";

export function createIndicators(
  indicators: IndicatorState["indicators"],
): Indicator[] {
  return [
    new EMAIndicator("ema20", 20, indicators.ema20),

    new EMAIndicator("ema50", 50, indicators.ema50),

    new EMAIndicator("ema200", 200, indicators.ema200),

    new SMAIndicator("sma20", 20, indicators.sma20),

    new SMAIndicator("sma50", 50, indicators.sma50),
  ];
}
