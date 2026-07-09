from sqlalchemy.orm import Session

from app.repositories.instrument_repository import InstrumentRepository
from app.repositories.ohlcv_repository import OHLCVRepository


class CandleService:
    """
    Service for historical candle retrieval.
    """

    def __init__(
        self,
        db: Session,
    ):

        self.instrument_repository = InstrumentRepository(db)
        self.ohlcv_repository = OHLCVRepository(db)

    def get_candles(
        self,
        symbol: str,
        timeframe: str,
        limit: int = 500,
    ):

        instrument = self.instrument_repository.get_by_symbol(
            symbol
        )

        if instrument is None:
            return []

        return self.ohlcv_repository.get_candles(
            instrument.id,
            timeframe,
            limit,
        )