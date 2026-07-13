import api from "./api";

export interface HistoryImportRequest {
  symbol: string;
  timeframe: string;
  limit: number;
}

export interface HistoryImportResponse {
  symbol: string;
  timeframe: string;
  requested: number;
  inserted: number;
  skipped: number;
}

export async function importHistory(
  symbol: string,
  timeframe = "1d",
  limit = 1000,
): Promise<HistoryImportResponse> {
  const response = await api.post<HistoryImportResponse>("/history/import", {
    symbol,
    timeframe,
    limit,
  });

  return response.data;
}
