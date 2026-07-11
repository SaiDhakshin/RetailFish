import axios from "axios";

import type {
  AddWatchlistItemRequest,
  CreateWatchlistRequest,
  RenameWatchlistRequest,
  Watchlist,
  WatchlistItem,
} from "@/types/watchlist";

const api = axios.create({
  baseURL: "/api",
});

export async function getWatchlists(): Promise<Watchlist[]> {
  const { data } = await api.get<Watchlist[]>("/watchlists");

  return data;
}

export async function createWatchlist(
  request: CreateWatchlistRequest,
): Promise<Watchlist> {
  const { data } = await api.post<Watchlist>(
    "/watchlists",
    request,
  );

  return data;
}

export async function renameWatchlist(
  watchlistId: number,
  request: RenameWatchlistRequest,
): Promise<Watchlist> {
  const { data } = await api.patch<Watchlist>(
    `/watchlists/${watchlistId}`,
    request,
  );

  return data;
}

export async function deleteWatchlist(
  watchlistId: number,
): Promise<void> {
  await api.delete(
    `/watchlists/${watchlistId}`,
  );
}

export async function getItems(
  watchlistId: number,
): Promise<WatchlistItem[]> {
  const { data } = await api.get<WatchlistItem[]>(
    `/watchlists/${watchlistId}/items`,
  );

  return data;
}

export async function addSymbol(
  watchlistId: number,
  request: AddWatchlistItemRequest,
): Promise<WatchlistItem> {
  const { data } = await api.post<WatchlistItem>(
    `/watchlists/${watchlistId}/items`,
    request,
  );

  return data;
}

export async function removeSymbol(
  watchlistId: number,
  instrumentId: number,
): Promise<void> {
  await api.delete(
    `/watchlists/${watchlistId}/items/${instrumentId}`,
  );
}