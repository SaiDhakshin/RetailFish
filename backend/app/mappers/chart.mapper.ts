import type {
  CandlestickData,
  UTCTimestamp,
} from "lightweight-charts";

import type { Candle } from "@/types/candle";

export class ChartMapper {
  static toCandlesticks(
    candles: Candle[],
  ): CandlestickData<UTCTimestamp>[] {
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