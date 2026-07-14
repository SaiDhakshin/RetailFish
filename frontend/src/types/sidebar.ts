export interface SidebarItem {
  symbol: string;

  price?: number;

  change?: number;

  changePercent?: number;

  score?: number;

  matchedFilters?: string[];

  watchlistItemId?: number;

  relativeStrength?: number;

  volumeRatio?: number;

  distanceFromHigh?: number;
}
