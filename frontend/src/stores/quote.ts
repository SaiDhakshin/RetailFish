import { defineStore } from "pinia";

import { getBulkQuotes, getQuote } from "@/services/quotes.service";

import type { Quote } from "@/types/quote";

export type QuoteMode = "manual" | "polling" | "realtime";

const DEFAULT_QUOTE_TTL = 15_000;
const DEFAULT_REFRESH_INTERVAL = 15_000;

interface CachedQuote {
  quote: Quote;
  expiresAt: number;
}

export const useQuoteStore = defineStore("quotes", {
  state: () => ({
    cache: {} as Record<string, CachedQuote>,
    activeSymbols: [] as string[],
    mode: "polling" as QuoteMode,
    refreshInterval: DEFAULT_REFRESH_INTERVAL,
    refreshTimer: null as number | null,
    pendingQuoteLoads: {} as Record<string, Promise<Quote> | undefined>,
  }),

  getters: {
    quote:
      (state) =>
      (symbol: string): Quote | undefined => {
        return state.cache[symbol]?.quote;
      },
  },

  actions: {
    async loadQuote(symbol: string) {
      const cached = this.quote(symbol);

      if (cached) {
        return cached;
      }

      const quote = await getQuote(symbol);

      this.cache[symbol] = {
        quote,
        expiresAt: Date.now() + DEFAULT_QUOTE_TTL,
      };

      return quote;
    },

    async loadQuotes(symbols: string[], force = false) {
      const uniqueSymbols = [...new Set(symbols)];

      if (uniqueSymbols.length === 0) {
        return;
      }

      const now = Date.now();
      const missingSymbols = force
        ? uniqueSymbols
        : uniqueSymbols.filter((symbol) => {
            const cached = this.cache[symbol];
            return !cached || cached.expiresAt < now;
          });

      if (missingSymbols.length === 0) {
        return;
      }

      const promises: Promise<Quote>[] = [];
      const symbolsToFetch = missingSymbols.filter(
        (symbol) => this.pendingQuoteLoads[symbol] === undefined,
      );

      for (const symbol of missingSymbols) {
        const pending = this.pendingQuoteLoads[symbol];
        if (pending !== undefined) {
          promises.push(pending);
        }
      }

      if (symbolsToFetch.length > 0) {
        const request = getBulkQuotes(symbolsToFetch)
          .then((quotes) => {
            const expiresAt = Date.now() + DEFAULT_QUOTE_TTL;

            for (const quote of quotes) {
              this.cache[quote.symbol] = {
                quote,
                expiresAt,
              };
              delete this.pendingQuoteLoads[quote.symbol];
            }

            return quotes;
          })
          .catch((error) => {
            for (const symbol of symbolsToFetch) {
              delete this.pendingQuoteLoads[symbol];
            }
            throw error;
          });

        for (const symbol of symbolsToFetch) {
          const symbolPromise = request.then((quotes) => {
            const quote = quotes.find((item) => item.symbol === symbol);
            if (!quote) {
              throw new Error(`Quote for ${symbol} missing from bulk response`);
            }
            return quote;
          });

          this.pendingQuoteLoads[symbol] = symbolPromise;
          promises.push(symbolPromise);
        }
      }

      await Promise.all(promises);
    },

    async refreshActiveSymbols() {
      if (this.activeSymbols.length === 0) {
        return;
      }

      await this.loadQuotes(this.activeSymbols, true);
    },

    clear() {
      this.cache = {};
    },

    async setActiveSymbols(symbols: string[]) {
      this.activeSymbols = [...new Set(symbols)];

      if (this.mode === "polling") {
        if (this.refreshTimer === null) {
          await this.startPolling();
        } else {
          await this.refreshActiveSymbols();
        }
        return;
      }

      if (this.mode === "manual") {
        await this.refreshActiveSymbols();
      }
    },

    async setQuoteMode(mode: QuoteMode) {
      if (this.mode === mode) {
        return;
      }

      this.mode = mode;

      if (mode === "polling") {
        await this.startPolling();
        return;
      }

      this.stopPolling();
      this.disconnectRealtime();
    },

    setRefreshInterval(intervalMs: number) {
      this.refreshInterval = Math.max(1_000, intervalMs);

      if (this.mode === "polling") {
        this.restartPolling();
      }
    },

    async startPolling() {
      if (this.mode !== "polling" || this.refreshTimer !== null) {
        return;
      }

      await this.refreshActiveSymbols();

      this.refreshTimer = window.setInterval(async () => {
        if (this.activeSymbols.length === 0) {
          return;
        }

        await this.loadQuotes(this.activeSymbols);
      }, this.refreshInterval);
    },

    stopPolling() {
      if (this.refreshTimer === null) {
        return;
      }

      clearInterval(this.refreshTimer);
      this.refreshTimer = null;
    },

    restartPolling() {
      this.stopPolling();
      void this.startPolling();
    },

    connectRealtime() {
      // Placeholder for future websocket / socket-based quote streaming.
    },

    disconnectRealtime() {
      // Placeholder to tear down any realtime connections in the future.
    },
  },
});
