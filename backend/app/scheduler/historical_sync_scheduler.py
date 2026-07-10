from __future__ import annotations

import logging
import time

from app.core.database import SessionLocal
from app.core.providers import get_market_data_provider
from app.core.settings import settings
from app.repositories.instrument_repository import InstrumentRepository
from app.services.historical_sync_service import HistoricalSyncService

logger = logging.getLogger(__name__)


class HistoricalSyncScheduler:
    """
    Background scheduler responsible for keeping
    historical market data synchronized.

    Responsibilities
    ----------------
    - Open a database session
    - Load all instruments
    - Synchronize configured timeframes
    - Log progress
    - Close the database session
    """

    def __init__(self) -> None:
        pass

    def sync_all_daily(self) -> None:
        """
        Synchronize all configured instruments.
        """

        db = SessionLocal()

        started_at = time.perf_counter()

        total = 0
        processed = 0
        updated = 0
        skipped = 0
        failed = 0
        candles_inserted = 0

        try:

            provider = get_market_data_provider()

            service = HistoricalSyncService(
                db=db,
                provider=provider,
            )

            repository = InstrumentRepository(db)

            instruments = repository.get_all()

            timeframes = [
                timeframe.strip()
                for timeframe in settings.HISTORY_SYNC_TIMEFRAMES.split(",")
            ]

            total = len(instruments) * len(timeframes)

            logger.info(
                "Starting scheduled historical sync (%d instruments, %d timeframe(s))...",
                len(instruments),
                len(timeframes),
            )

            for instrument in instruments:

                for timeframe in timeframes:

                    try:

                        result = service.sync_latest(
                            symbol=instrument.symbol,
                            timeframe=timeframe,
                        )

                        processed += 1

                        inserted = result["inserted"]

                        candles_inserted += inserted

                        if inserted > 0:
                            updated += 1
                        else:
                            skipped += 1

                    except Exception:

                        processed += 1
                        failed += 1

                        logger.exception(
                            "Failed syncing %s (%s)",
                            instrument.symbol,
                            timeframe,
                        )

                    if (
                        processed % 100 == 0
                        or processed == total
                    ):

                        progress = (
                            processed / total
                        ) * 100

                        logger.info(
                            "Progress: %d/%d (%.1f%%) | Updated=%d | Skipped=%d | Failed=%d | Candles=%d",
                            processed,
                            total,
                            progress,
                            updated,
                            skipped,
                            failed,
                            candles_inserted,
                        )

            elapsed = time.perf_counter() - started_at

            logger.info("")
            logger.info("=" * 70)
            logger.info("Historical Sync Completed")
            logger.info("=" * 70)
            logger.info("Total Instruments : %d", len(instruments))
            logger.info("Timeframes         : %s", ", ".join(timeframes))
            logger.info("Tasks Processed    : %d", processed)
            logger.info("Updated            : %d", updated)
            logger.info("Skipped            : %d", skipped)
            logger.info("Failed             : %d", failed)
            logger.info("Candles Inserted   : %d", candles_inserted)
            logger.info("Elapsed            : %.2f seconds", elapsed)
            logger.info("=" * 70)

        finally:

            db.close()