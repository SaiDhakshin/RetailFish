from dataclasses import dataclass, field


@dataclass(slots=True)
class ScanResult:
    symbol: str

    score: int

    matched_filters: list[str]