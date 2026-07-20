export interface ScanDetail {
  filter: string;
  value: string;
}

import type { ChartOverlay } from "@/types/overlay";

export interface ScannerResult {
  symbol: string;

  score: number;

  matched_filters: string[];

  details: ScanDetail[];

  relative_strength: number;

  volume_ratio: number;

  distance_from_high: number;

  overlays?: ChartOverlay[];
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
  DOUBLE_BOTTOM: "double_bottom",
  DOUBLE_TOP: "double_top",
  HEAD_SHOULDERS: "head_shoulders",
  INVERSE_HEAD_SHOULDERS: "inverse_head_shoulders",
  TRIANGLES: "triangles",
  FLAGS: "flags",
  HARMONICS: "harmonics",
  TRENDLINES: "trendlines",
  TREND_TEMPLATE: "trend_template",
} as const;

export type ScanFilter = (typeof ScanFilter)[keyof typeof ScanFilter];
