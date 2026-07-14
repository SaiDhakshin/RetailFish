from dataclasses import dataclass, field
from app.scanner.models.scan_detail import (
    ScanDetail,
)


@dataclass(slots=True)
class ScanResult:
    symbol: str

    score: int

    matched_filters: list[str]

    details: list[ScanDetail]

    relative_strength: float = 0

    volume_ratio: float = 0

    distance_from_high: float = 0
