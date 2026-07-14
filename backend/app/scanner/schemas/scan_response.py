from pydantic import BaseModel


class ScanDetailResponse(BaseModel):
    filter: str

    value: str


class ScanResponse(BaseModel):
    symbol: str

    score: int

    matched_filters: list[str]

    details: list[ScanDetailResponse]

    relative_strength: float

    volume_ratio: float

    distance_from_high: float