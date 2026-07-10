export const TIMEFRAMES = [
  {
    label: "1m",
    value: "1m",
  },
  {
    label: "5m",
    value: "5m",
  },
  {
    label: "15m",
    value: "15m",
  },
  {
    label: "1h",
    value: "1h",
  },
  {
    label: "1D",
    value: "1d",
  },
  {
    label: "1W",
    value: "1wk",
  },
  {
    label: "1M",
    value: "1mo",
  },
] as const;

export type TimeFrame =
  typeof TIMEFRAMES[number]["value"];