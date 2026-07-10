from abc import ABC, abstractmethod
from typing import Any

from app.dto.market_data import MarketDataDTO

class MarketDataProvider(ABC):
    """
    Abstract interface for all market data providers.

    Every provider (Yahoo Finance, Binance, NSE, etc.)
    must implement this interface.
    """

    @abstractmethod
    def fetch_historical(
        self,
        symbol: str,
        timeframe: str,
        limit: int = 500,
    ) -> list[MarketDataDTO]:
        """
        Fetch historical OHLCV candles.

        Returns a normalized list of candles.

        Example:

        [
            {
                "timestamp": datetime,
                "open": float,
                "high": float,
                "low": float,
                "close": float,
                "volume": float,
            }
        ]
        """
        raise NotImplementedError