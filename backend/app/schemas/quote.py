from datetime import datetime

from pydantic import BaseModel


class QuoteResponse(BaseModel):
    """
    Latest market quote.
    """

    symbol: str

    price: float

    previous_close: float

    change: float

    change_percent: float

    currency: str

    exchange: str

    timestamp: datetime

class BulkQuoteResponse(BaseModel):
    """
    Response containing multiple quotes.
    """

    quotes: list[QuoteResponse]