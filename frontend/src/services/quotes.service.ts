import axios from "axios";

import type { Quote } from "@/types/quote";

const api = axios.create({
  baseURL: "/api",
});

export async function getQuote(symbol: string): Promise<Quote> {
  const { data } = await api.get<Quote>("/quotes", {
    params: {
      symbol,
    },
  });

  return data;
}

export async function getQuotes(symbols: string[]): Promise<Quote[]> {
  const { data } = await api.get("/quotes/bulk", {
    params: {
      symbols: symbols.join(","),
    },
  });

  return data.quotes;
}
