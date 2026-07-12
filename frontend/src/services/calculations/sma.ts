import type { LineData, UTCTimestamp } from "lightweight-charts";

import type { Candle } from "@/types/candle";

export function calculateSMA(
  candles: Candle[],
  period: number,
): LineData<UTCTimestamp>[] {
  if (candles.length < period) {
    return [];
  }

  const result: LineData<UTCTimestamp>[] = [];

  for (let i = period - 1; i < candles.length; i++) {
    let sum = 0;

    for (let j = i - period + 1; j <= i; j++) {
      sum += candles[j].close;
    }

    result.push({
      time: Math.floor(
        new Date(candles[i].timestamp).getTime() / 1000,
      ) as UTCTimestamp,

      value: Number((sum / period).toFixed(2)),
    });
  }

  return result;
}
