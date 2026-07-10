from pydantic import BaseModel


class HistorySyncResponse(BaseModel):
    symbol: str
    timeframe: str
    downloaded: int
    inserted: int
    skipped: int