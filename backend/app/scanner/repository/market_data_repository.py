from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.instrument import Instrument
from app.models.ohlcv import OHLCV


class MarketDataRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_instruments(
        self,
    ) -> list[Instrument]:
        return list(
            self.db.scalars(
                select(Instrument).order_by(
                    Instrument.symbol,
                )
            )
        )

    def get_candles(
        self,
        instrument_id: int,
        timeframe: str,
        limit: int,
    ) -> list[OHLCV]:
        candles = list(
            self.db.scalars(
                select(OHLCV)
                .where(
                    OHLCV.instrument_id == instrument_id,
                    OHLCV.timeframe == timeframe,
                )
                .order_by(
                    OHLCV.timestamp.desc(),
                )
                .limit(limit)
            )
        )

        candles.reverse()

        return candles