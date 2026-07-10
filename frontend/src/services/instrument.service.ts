import api from "./api";
import type { InstrumentSearchResponse } from "../types/instrument";

export async function searchInstruments(
    query: string,
) {
    const response =
        await api.get<InstrumentSearchResponse>(
            "/instruments",
            {
                params: {
                    q: query,
                },
            },
        );

    return response.data;
}