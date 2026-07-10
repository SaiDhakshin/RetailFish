import api from "./api";
import type { Candle } from "@/types/candle";

export async function getCandles(
    symbol: string,
) {
    const response =
        await api.get<Candle[]>(
            "/candles",
            {
                params: {
                    symbol,
                    timeframe: "1d",
                    limit: 500,
                },
            },
        );

    return response.data;
}