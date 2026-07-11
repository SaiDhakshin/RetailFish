import type { Quote } from "./quote";

export interface SearchResult {
  id: number;

  symbol: string;

  name: string;

  exchange: string;

  quote?: Quote;
}
