from dataclasses import dataclass, field
from app.scanner.models.scan_detail import (
    ScanDetail,
)

@dataclass(slots=True)
class ScanResult:
    symbol: str

    score: int

    matched_filters: list[str]

    details: dict[ScanDetail]