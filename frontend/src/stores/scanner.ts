import { defineStore } from "pinia";

import { runScanner } from "@/services/scanner.service";

import type { ScanRequest } from "@/services/scanner.service";

import type { ScannerResult } from "@/types/scanner";

export const useScannerStore = defineStore("scanner", {
  state: () => ({
    results: [] as ScannerResult[],

    loading: false,

    selectedSymbol: null as string | null,

    selectedResult: null as ScannerResult | null,

    sortBy: "score" as
      | "score"
      | "relative_strength"
      | "volume_ratio"
      | "distance_from_high"
      | "symbol",

    sortDirection: "desc" as "asc" | "desc",
  }),

  getters: {
    sortedResults(state): ScannerResult[] {
      const results = [...state.results];

      results.sort((a, b) => {
        let comparison = 0;

        switch (state.sortBy) {
          case "score":
            comparison = a.score - b.score;
            break;

          case "relative_strength":
            comparison = a.relative_strength - b.relative_strength;
            break;

          case "volume_ratio":
            comparison = a.volume_ratio - b.volume_ratio;
            break;

          case "distance_from_high":
            comparison = a.distance_from_high - b.distance_from_high;
            break;

          case "symbol":
            comparison = a.symbol.localeCompare(b.symbol);
            break;
        }

        return state.sortDirection === "asc" ? comparison : -comparison;
      });

      return results;
    },
  },

  actions: {
    async scan(request: ScanRequest) {
      this.loading = true;

      try {
        this.results = await runScanner(request);

        if (this.results.length > 0) {
          this.selectResult(this.results[0]);
        }
      } finally {
        this.loading = false;
      }
    },

    clear() {
      this.results = [];
      this.selectedSymbol = null;
      this.selectedResult = null;
    },

    selectSymbol(symbol: string) {
      this.selectedSymbol = symbol;
      // Also update selectedResult for consistency
      const result = this.results.find((r) => r.symbol === symbol);
      if (result) {
        this.selectedResult = result;
      }
    },

    selectResult(result: ScannerResult) {
      this.selectedResult = result;
      this.selectedSymbol = result.symbol;
    },
  },
});
