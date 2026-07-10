from __future__ import annotations

from app.dto.market_data import MarketDataDTO
from app.models.ohlcv import OHLCV


class MarketDataMapper:
    """
    Maps provider DTOs to database models.
    """

    @staticmethod
    def to_ohlcv_models(
        candles: list[MarketDataDTO],
        instrument_id: int,
        timeframe: str,
    ) -> list[OHLCV]:
        """
        Convert MarketDataDTO objects into OHLCV models.
        """

        return [
            OHLCV(
                instrument_id=instrument_id,
                timeframe=timeframe,
                timestamp=candle.timestamp,
                open=candle.open,
                high=candle.high,
                low=candle.low,
                close=candle.close,
                volume=candle.volume,
            )
            for candle in candles
        ]