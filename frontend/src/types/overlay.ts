export type ChartOverlayType =
  | "polyline"
  | "horizontalLine"
  | "label"
  | "marker";

export interface ChartPoint {
  time: string | number | Date;
  value: number;
}

export interface ChartOverlay {
  id: string;
  type: ChartOverlayType;
  color: string;
  points: ChartPoint[];
  text?: string;
}
