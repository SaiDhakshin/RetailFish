from __future__ import annotations

from sqlalchemy.orm import Session

from app.clients.market_data_provider import MarketDataProvider
from app.core.logger import logger
from app.exceptions.instrument import InstrumentNotFoundError
from app.mappers.market_data_mapper import MarketDataMapper
from app.models.instrument import Instrument
from app.models.ohlcv import OHLCV
from app.repositories.instrument_repository import InstrumentRepository
from app.repositories.ohlcv_repository import OHLCVRepository


class MarketDataService:
    """
    Coordinates all market data operations.

    Responsibilities
    ----------------
    - Ensure historical data exists
    - Download missing candles
    - Convert provider DTOs into database models
    - Persist market data
    """

    def __init__(
        self,
        db: Session,
        provider: MarketDataProvider,
    ) -> None:
        self.provider = provider

        self.instrument_repository = InstrumentRepository(db)
        self.ohlcv_repository = OHLCVRepository(db)

    def ensure_history(
        self,
        symbol: str,
        timeframe: str,
        limit: int = 500,
    ) -> list[OHLCV]:
        """
        Return historical candles.

        If the database does not contain candles,
        they are downloaded, saved and returned.
        """

        instrument = self._get_instrument(symbol)

        candles = self.ohlcv_repository.get_candles(
            instrument_id=instrument.id,
            timeframe=timeframe,
            limit=limit,
        )

        if candles:
            logger.info("Cache hit for %s", symbol)
            return candles

        logger.info("Cache miss for %s", symbol)

        return self.backfill(
            instrument=instrument,
            timeframe=timeframe,
            limit=limit,
        )

    def backfill(
        self,
        instrument: Instrument,
        timeframe: str,
        limit: int = 500,
    ) -> list[OHLCV]:
        """
        Download historical candles,
        save them to PostgreSQL,
        and return the saved models.
        """

        logger.info(
            "Downloading %s (%s)",
            instrument.symbol,
            timeframe,
        )

        candles = self.provider.fetch_historical(
            symbol=instrument.symbol,
            timeframe=timeframe,
            limit=limit,
        )

        models = MarketDataMapper.to_ohlcv_models(
            candles=candles,
            instrument_id=instrument.id,
            timeframe=timeframe,
        )

        inserted = self.ohlcv_repository.save_bulk(models)

        logger.info(
            "Backfill complete | symbol=%s inserted=%s skipped=%s",
            instrument.symbol,
            inserted,
            len(models) - inserted,
        )

        return self.ohlcv_repository.get_candles(
            instrument_id=instrument.id,
            timeframe=timeframe,
            limit=limit,
        )

    def backfill_summary(
        self,
        symbol: str,
        timeframe: str,
        limit: int = 500,
    ) -> dict:
        """
        Backfill history and return a summary.
        Used by manual import endpoints.
        """

        instrument = self._get_instrument(symbol)

        candles = self.provider.fetch_historical(
            symbol=instrument.symbol,
            timeframe=timeframe,
            limit=limit,
        )

        models = MarketDataMapper.to_ohlcv_models(
            candles=candles,
            instrument_id=instrument.id,
            timeframe=timeframe,
        )

        inserted = self.ohlcv_repository.save_bulk(models)

        return {
            "symbol": instrument.symbol,
            "timeframe": timeframe,
            "requested": len(models),
            "inserted": inserted,
            "skipped": len(models) - inserted,
        }

    def _get_instrument(
        self,
        symbol: str,
    ) -> Instrument:
        """
        Return the instrument or raise an exception.
        """

        instrument = self.instrument_repository.get_by_symbol(
            symbol
        )

        if instrument is None:
            raise InstrumentNotFoundError(symbol)

        return instrument