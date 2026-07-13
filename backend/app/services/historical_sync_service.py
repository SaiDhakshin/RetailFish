from sqlalchemy.orm import Session

from app.services.market_data_service import MarketDataService
from app.clients.market_data_provider import MarketDataProvider


class HistoricalSyncService:
    """
    Service responsible for coordinating historical market data
    synchronization across one or more instruments.

    This service orchestrates higher-level synchronization workflows
    while delegating the actual download and persistence of market data
    to MarketDataService.
    """

    def __init__(self, db: Session, provider: MarketDataProvider) -> None:
        """
        Initialize the historical synchronization service.

        Args:
            db: SQLAlchemy database session.
        """
        self.db = db
        self.market_data_service = MarketDataService(db,provider)

    def sync(
        self,
        symbol: str,
        timeframe: str,
        limit: int = 1000,
    ):
        return self.market_data_service.backfill_by_symbol(
            symbol=symbol,
            timeframe=timeframe,
            limit=limit,
        )
    
    def sync_all(
        self,
        symbols: list[str],
        timeframe: str,
        limit: int = 1000,
    ) -> dict:
        """
        Synchronize historical data for multiple instruments.
        """

        results = []

        total_requested = 0
        total_inserted = 0
        total_skipped = 0

        for symbol in symbols:
            result = self.sync(
                symbol=symbol,
                timeframe=timeframe,
                limit=limit,
            )

            results.append(result)

            total_requested += result["requested"]
            total_inserted += result["inserted"]
            total_skipped += result["skipped"]

        return {
            "symbols": len(symbols),
            "timeframe": timeframe,
            "requested": total_requested,
            "inserted": total_inserted,
            "skipped": total_skipped,
            "results": results,
        }
    
    def sync_latest(
        self,
        symbol: str,
        timeframe: str,
    ) -> dict:
        return self.market_data_service.sync_latest_by_symbol(
            symbol=symbol,
            timeframe=timeframe,
        )
    