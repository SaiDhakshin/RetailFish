from pydantic import BaseModel


class HistoryImportRequest(BaseModel):
    symbol: str
    timeframe: str = "1d"
    limit: int = 1000


class HistoryImportResponse(BaseModel):
    symbol: str
    timeframe: str
    requested: int
    inserted: int
    skipped: int