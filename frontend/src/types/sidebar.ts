export interface SidebarItem {
  symbol: string;

  price?: number;

  change?: number;

  changePercent?: number;

  score?: number;

  matchedFilters?: string[];

  watchlistItemId?: number;
}
