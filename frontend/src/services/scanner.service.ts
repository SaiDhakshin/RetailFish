import api from "./api";

import type { ScannerResult, ScanUniverse, ScanFilter } from "@/types/scanner";

export interface ScanRequest {
  universe: ScanUniverse;
  filters: ScanFilter[];
}

export async function runScanner(
  request: ScanRequest,
): Promise<ScannerResult[]> {
  const response = await api.post<ScannerResult[]>("/scanner/run", request);

  return response.data;
}
