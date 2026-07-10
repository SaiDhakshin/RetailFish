import api from "./api";
import type { Candle } from "@/types/candle";
import type { TimeFrame } from "@/types/timeframe";

export async function getCandles(
    symbol: string,
    timeframe: TimeFrame,
) {
    const response =
        await api.get<Candle[]>(
            "/candles",
            {
                params: {
                    symbol,
                    timeframe,
                    limit: 500,
                },
            },
        );

    return response.data;
}