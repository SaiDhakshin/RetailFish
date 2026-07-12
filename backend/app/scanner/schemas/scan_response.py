from pydantic import BaseModel


class ScanResponse(BaseModel):
    symbol: str

    score: int

    matched_filters: list[str]