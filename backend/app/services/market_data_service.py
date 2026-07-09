from sqlalchemy.orm import Session

from app.clients.market_data_provider import MarketDataProvider
from app.models.ohlcv import OHLCV
from app.repositories.instrument_repository import InstrumentRepository
from app.repositories.ohlcv_repository import OHLCVRepository


class MarketDataService:
    """
    Service responsible for downloading,
    transforming and storing market data.
    """

    def __init__(
        self,
        db: Session,
        provider: MarketDataProvider,
    ):

        self.db = db
        self.provider = provider

        self.instrument_repository = InstrumentRepository(db)
        self.ohlcv_repository = OHLCVRepository(db)

    def backfill(
        self,
        symbol: str,
        timeframe: str,
        limit: int = 500,
    ) -> dict:

        instrument = self.instrument_repository.get_by_symbol(symbol)

        if instrument is None:
            raise ValueError(f"Instrument '{symbol}' not found.")

        candles = self.provider.fetch_historical(
            symbol=symbol,
            timeframe=timeframe,
            limit=limit,
        )

        ohlcv_models = [
            OHLCV(
                instrument_id=instrument.id,
                timeframe=timeframe,
                timestamp=candle["timestamp"],
                open=candle["open"],
                high=candle["high"],
                low=candle["low"],
                close=candle["close"],
                volume=candle["volume"],
            )
            for candle in candles
        ]

        inserted = self.ohlcv_repository.save_bulk(
            ohlcv_models
        )

        return {
            "symbol": symbol,
            "timeframe": timeframe,
            "requested": len(ohlcv_models),
            "inserted": inserted,
            "skipped": len(ohlcv_models) - inserted,
        }