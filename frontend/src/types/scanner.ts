export interface ScanDetail {
  filter: string;
  value: string;
}

export interface ScannerResult {
  symbol: string;

  score: number;

  matched_filters: string[];

  details?: ScanDetail[];
}

export const ScanUniverse = {
  NIFTY50: "nifty50",
  NIFTY100: "nifty100",
  NIFTY200: "nifty200",
  NIFTY500: "nifty500",
  ALL: "all",
} as const;

export type ScanUniverse = (typeof ScanUniverse)[keyof typeof ScanUniverse];

export const ScanFilter = {
  EMA_ALIGNMENT: "ema_alignment",
  FIFTY_TWO_WEEK_HIGH: "fifty_two_week_high",
  VOLUME_BREAKOUT: "volume_breakout",
  RELATIVE_STRENGTH: "relative_strength",
  CUP_HANDLE: "cup_handle",
  VCP: "vcp",
} as const;

export type ScanFilter = (typeof ScanFilter)[keyof typeof ScanFilter];
