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

import { useQuoteStore } from "@/stores/quote";

import type { Watchlist, WatchlistItem } from "@/types/watchlist";

export const useWatchlistStore = defineStore("watchlists", {
  state: () => ({
    watchlists: [] as Watchlist[],

    selectedWatchlist: null as Watchlist | null,

    items: [] as WatchlistItem[],

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
      const quoteStore = useQuoteStore();

      try {
        this.items = await getItems(watchlistId);

        await quoteStore.setActiveSymbols(
          this.items.map((item) => item.symbol),
        );
      } finally {
        this.loading = false;
      }
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
        }
      }
    },

    async addSymbol(watchlistId: number, symbol: string) {
      const quoteStore = useQuoteStore();
      try {
        await addSymbol(watchlistId, {
          symbol,
        });

        if (this.selectedWatchlist?.id === watchlistId) {
          this.items = await getItems(watchlistId);

          await quoteStore.setActiveSymbols(
            this.items.map((item) => item.symbol),
          );
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
      const quoteStore = useQuoteStore();

      await removeSymbol(this.selectedWatchlist.id, instrumentId);

      this.items = await getItems(this.selectedWatchlist.id);

      await quoteStore.setActiveSymbols(this.items.map((item) => item.symbol));
    },

    selectSymbol(symbol: string) {
      this.selectedSymbol = symbol;
    },
  },
});
