from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CandleResponse(BaseModel):
    """
    Response model for a candle.
    """

    model_config = ConfigDict(from_attributes=True)

    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float