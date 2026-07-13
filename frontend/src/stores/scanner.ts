import { defineStore } from "pinia";

import { runScanner } from "@/services/scanner.service";

import type { ScanRequest } from "@/services/scanner.service";

import type { ScannerResult } from "@/types/scanner";

export const useScannerStore = defineStore("scanner", {
  state: () => ({
    results: [] as ScannerResult[],

    loading: false,

    selectedSymbol: null as string | null,
  }),

  actions: {
    async scan(request: ScanRequest) {
      this.loading = true;

      try {
        this.results = await runScanner(request);

        if (this.results.length > 0) {
          this.selectedSymbol = this.results[0].symbol;
        }
      } finally {
        this.loading = false;
      }
    },

    clear() {
      this.results = [];
      this.selectedSymbol = null;
    },

    selectSymbol(symbol: string) {
      this.selectedSymbol = symbol;
    },
  },
});
