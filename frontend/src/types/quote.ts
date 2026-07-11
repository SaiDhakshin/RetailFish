export interface Quote {
  symbol: string;

  price: number;

  previous_close: number;

  change: number;

  change_percent: number;

  currency: string;

  exchange: string;

  timestamp: string;
}
