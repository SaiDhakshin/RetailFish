from dataclasses import dataclass


@dataclass(slots=True)
class SyncResult:
    symbol: str
    status: str  # updated | skipped | failed
    candles_inserted: int