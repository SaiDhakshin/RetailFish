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

export async function getBulkQuotes(symbols: string[]): Promise<Quote[]> {
  const { data } = await api.post("/quotes/bulk", {
    symbols,
  });

  console.log("Bulk response:", data);
  console.log("Returning:", data.quotes);

  // Normalize response to an array of Quote
  if (Array.isArray(data)) {
    return data as Quote[];
  }

  if (Array.isArray(data.quotes)) {
    return data.quotes as Quote[];
  }

  if (data.quotes && typeof data.quotes === "object") {
    return Object.values(data.quotes) as Quote[];
  }

  // Fallback: return empty array to avoid iteration errors
  return [];
}

export async function getQuotes(symbols: string[]): Promise<Quote[]> {
  const { data } = await api.get("/quotes/bulk", {
    params: {
      symbols: symbols.join(","),
    },
  });

  return data.quotes;
}
