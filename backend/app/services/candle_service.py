from sqlalchemy.orm import Session

from app.core.providers import (
    get_market_data_provider,
)
from app.services.market_data_service import (
    MarketDataService,
)


class CandleService:
    """
    Read-only candle service.

    Delegates market data lifecycle
    to MarketDataService.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        provider = get_market_data_provider()

        self.market_data_service = (
            MarketDataService(
                db=db,
                provider=provider,
            )
        )

    def get_candles(
        self,
        symbol: str,
        timeframe: str,
        limit: int = 1000,
    ):

        return self.market_data_service.ensure_history(
            symbol=symbol,
            timeframe=timeframe,
            limit=limit,
        )