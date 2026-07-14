from dataclasses import dataclass, field


@dataclass(slots=True)
class ScanDetail:
    filter: str

    value: str


@dataclass(slots=True)
class ScanResult:
    symbol: str

    score: int

    matched_filters: list[str]

    details: list[ScanDetail] = field(default_factory=list)
