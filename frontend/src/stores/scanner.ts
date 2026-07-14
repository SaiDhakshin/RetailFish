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
  }),

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
