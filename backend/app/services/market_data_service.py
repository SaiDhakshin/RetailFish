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
from datetime import datetime
from app.dto.market_data import MarketDataDTO

from app.core.database import SessionLocal

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed


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
        limit: int = 1000,
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
            self.sync_latest(
                instrument=instrument,
                timeframe=timeframe,
            )

            return self.ohlcv_repository.get_candles(
                instrument_id=instrument.id,
                timeframe=timeframe,
                limit=limit,
            )

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
        limit: int = 1000,
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

        if not candles:
            logger.info(
                "No historical data found for %s",
                instrument.symbol,
            )

            return []

        models, inserted = self._save_market_data(
            instrument=instrument,
            timeframe=timeframe,
            candles=candles,
        )

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
        limit: int = 1000,
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

    def _save_market_data(
        self,
        instrument: Instrument,
        timeframe: str,
        candles: list[MarketDataDTO],
    ) -> tuple[list[OHLCV], int]:
        """
        Convert provider DTOs into OHLCV models,
        persist them, and return the saved models
        together with the number of inserted rows.
        """

        models = MarketDataMapper.to_ohlcv_models(
            candles=candles,
            instrument_id=instrument.id,
            timeframe=timeframe,
        )

        inserted = self.ohlcv_repository.save_bulk(
            models
        )

        return models, inserted

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
    
    def sync_latest(
        self,
        instrument: Instrument,
        timeframe: str,
    ) -> dict:
        """
        Download only candles newer than the latest
        candle stored in the database.
        """

        latest_timestamp = (
            self.ohlcv_repository.get_latest_timestamp(
                instrument_id=instrument.id,
                timeframe=timeframe,
            )
        )

        logger.info(
            "Incremental sync | symbol=%s timeframe=%s latest=%s",
            instrument.symbol,
            timeframe,
            latest_timestamp,
        )

        candles = self.provider.fetch_historical(
            symbol=instrument.symbol,
            timeframe=timeframe,
            start=latest_timestamp,
        )

        if not candles:
            logger.info(
                "No new candles for %s",
                instrument.symbol,
            )

            return {
                "symbol": instrument.symbol,
                "timeframe": timeframe,
                "downloaded": 0,
                "inserted": 0,
                "skipped": 0,
            }

        models, inserted = self._save_market_data(
            instrument=instrument,
            timeframe=timeframe,
            candles=candles,
        )

        logger.info(
            "Incremental sync complete | symbol=%s downloaded=%s inserted=%s",
            instrument.symbol,
            len(models),
            inserted,
        )

        return {
            "symbol": instrument.symbol,
            "timeframe": timeframe,
            "downloaded": len(models),
            "inserted": inserted,
            "skipped": len(models) - inserted,
        }
    
    def backfill_by_symbol(
        self,
        symbol: str,
        timeframe: str,
        limit: int = 1000,
    ) -> list[OHLCV]:
        """
        Download and store historical candles for a symbol.
        """

        instrument = self._get_instrument(symbol)

        return self.backfill(
            instrument=instrument,
            timeframe=timeframe,
            limit=limit,
        )

    def sync_latest_by_symbol(
        self,
        symbol: str,
        timeframe: str,
    ) -> dict:
        """
        Synchronize only new candles for a symbol.
        """

        instrument = self._get_instrument(symbol)

        return self.sync_latest(
            instrument=instrument,
            timeframe=timeframe,
        )
