import type { Candle } from "@/types/candle";

import type { LineData, UTCTimestamp } from "lightweight-charts";

export function calculateEMA(
  candles: Candle[],
  period: number,
): LineData<UTCTimestamp>[] {
  if (candles.length === 0) {
    return [];
  }

  const multiplier = 2 / (period + 1);

  let ema = candles[0].close;

  const result: LineData<UTCTimestamp>[] = [];

  for (let i = 0; i < candles.length; i++) {
    const candle = candles[i];

    if (i === 0) {
      ema = candle.close;
    } else {
      ema = (candle.close - ema) * multiplier + ema;
    }

    result.push({
      time: Math.floor(
        new Date(candle.timestamp).getTime() / 1000,
      ) as UTCTimestamp,

      value: Number(ema.toFixed(2)),
    });
  }

  return result;
}
