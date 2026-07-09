import logging

from sqlalchemy.orm import Session

from app.services.historical_sync_service import HistoricalSyncService
from app.clients.market_data_provider import MarketDataProvider


logger = logging.getLogger(__name__)


class HistoricalSyncScheduler:
    """
    Coordinates scheduled historical market data synchronization.

    This class is responsible for invoking the historical
    synchronization workflow while handling logging and errors.
    """

    def __init__(self, db: Session, provider: MarketDataProvider) -> None:
        """
        Initialize the scheduler.

        Args:
            db: SQLAlchemy database session.
        """
        self.db = db
        self.sync_service = HistoricalSyncService(db,provider)

    def run_once(
        self,
        symbols: list[str],
        timeframe: str,
        limit: int = 500,
    ) -> dict:
        """
        Execute a single historical synchronization.

        Args:
            symbols: Symbols to synchronize.
            timeframe: Candle timeframe.
            limit: Number of candles to download.

        Returns:
            Synchronization summary.
        """

        logger.info("Starting historical synchronization...")

        try:
            result = self.sync_service.sync_all(
                symbols=symbols,
                timeframe=timeframe,
                limit=limit,
            )

            logger.info(
                "Synchronization completed. "
                "Inserted=%s Skipped=%s",
                result["inserted"],
                result["skipped"],
            )

            return result

        except Exception:
            logger.exception("Historical synchronization failed.")
            raise