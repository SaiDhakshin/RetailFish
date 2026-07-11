export interface Instrument {
  id: number;
  symbol: string;
  name: string;
}

export interface InstrumentSearchResponse {
  total: number;
  items: Instrument[];
}
