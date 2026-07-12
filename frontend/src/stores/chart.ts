import { defineStore } from "pinia";

interface ChartState {
  showVolume: boolean;
}

export const useChartStore = defineStore("chart", {
  state: (): ChartState => ({
    showVolume: true,
  }),

  actions: {
    toggleVolume() {
      this.showVolume = !this.showVolume;
    },
  },
});
