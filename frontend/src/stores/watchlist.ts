import { defineStore } from "pinia";

import {
  addSymbol,
  createWatchlist,
  deleteWatchlist,
  getItems,
  getWatchlists,
  removeSymbol,
  renameWatchlist,
} from "@/services/watchlists.service";

import { getQuote } from "@/services/quotes.service";

import type { Watchlist, WatchlistItem } from "@/types/watchlist";

import type { Quote } from "@/types/quote";

export const useWatchlistStore = defineStore("watchlists", {
  state: () => ({
    watchlists: [] as Watchlist[],

    selectedWatchlist: null as Watchlist | null,

    items: [] as WatchlistItem[],

    quotes: {} as Record<string, Quote>,

    loading: false,

    selectedSymbol: null as string | null,
  }),
  actions: {
    async loadWatchlists() {
      this.loading = true;

      try {
        this.watchlists = await getWatchlists();

        if (this.watchlists.length > 0 && this.selectedWatchlist === null) {
          this.selectedWatchlist = this.watchlists[0];

          await this.loadItems(this.selectedWatchlist.id);
        }
      } finally {
        this.loading = false;
      }
    },

    async loadItems(watchlistId: number) {
      this.loading = true;

      try {
        this.items = await getItems(watchlistId);

        await this.loadQuotes();
      } finally {
        this.loading = false;
      }
    },

    async loadQuote(symbol: string) {
      try {
        const quote = await getQuote(symbol);

        this.quotes[symbol] = quote;
      } catch (error) {
        console.error(`Failed loading quote for ${symbol}`, error);
      }
    },

    async loadQuotes() {
      const requests = this.items.map((item) => this.loadQuote(item.symbol));

      await Promise.all(requests);
    },

    async selectWatchlist(watchlist: Watchlist) {
      this.selectedWatchlist = watchlist;

      await this.loadItems(watchlist.id);
    },

    async createWatchlist(name: string) {
      const watchlist = await createWatchlist({
        name,
      });

      this.watchlists.push(watchlist);

      this.selectedWatchlist = watchlist;

      this.items = [];

      this.quotes = {};
    },

    async renameWatchlist(id: number, name: string) {
      const updated = await renameWatchlist(id, {
        name,
      });

      const index = this.watchlists.findIndex((w) => w.id === id);

      if (index !== -1) {
        this.watchlists[index] = updated;
      }
    },

    async deleteWatchlist(id: number) {
      await deleteWatchlist(id);

      this.watchlists = this.watchlists.filter((w) => w.id !== id);

      if (this.selectedWatchlist?.id === id) {
        this.selectedWatchlist = this.watchlists[0] ?? null;

        if (this.selectedWatchlist) {
          await this.loadItems(this.selectedWatchlist.id);
        } else {
          this.items = [];
          this.quotes = {};
        }
      }
    },

    async addSymbol(watchlistId: number, symbol: string) {
      try {
        await addSymbol(watchlistId, {
          symbol,
        });

        if (this.selectedWatchlist?.id === watchlistId) {
          this.items = await getItems(watchlistId);

          await this.loadQuotes();
        }
      } catch (error: any) {
        if (error.response?.status === 409) {
          alert(error.response.data.detail);

          return;
        }

        throw error;
      }
    },

    async removeSymbol(instrumentId: number) {
      if (!this.selectedWatchlist) {
        return;
      }

      await removeSymbol(this.selectedWatchlist.id, instrumentId);

      this.items = await getItems(this.selectedWatchlist.id);

      await this.loadQuotes();
    },

    selectSymbol(symbol: string) {
      this.selectedSymbol = symbol;
    },
  },
});
