export interface Watchlist {
  id: number;
  name: string;
  created_at: string;
  updated_at: string;
}

export interface WatchlistItem {
  id: number;              // watchlist item id
  instrument_id: number;   // instrument id
  symbol: string;
  created_at: string;
}

export interface CreateWatchlistRequest {
  name: string;
}

export interface RenameWatchlistRequest {
  name: string;
}

export interface AddWatchlistItemRequest {
  symbol: string;
}