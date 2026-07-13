from abc import ABC, abstractmethod

from app.schemas.candle import CandleResponse
from app.schemas.quote import QuoteResponse


class MarketDataProvider(ABC):
    """
    Base interface implemented by every market data provider.

    Examples:
    - Yahoo Finance
    - Upstox
    - Polygon.io
    - Binance
    """

    @abstractmethod
    def fetch_historical(
        self,
        symbol: str,
        timeframe: str,
        limit: int = 1000,
    ) -> list[CandleResponse]:
        """
        Download historical candles.
        """
        raise NotImplementedError

    @abstractmethod
    def fetch_quote(
        self,
        symbol: str,
    ) -> QuoteResponse:
        """
        Return the latest market quote.
        """
        raise NotImplementedError
    
    @abstractmethod
    def fetch_quotes(
        self,
        symbols: list[str],
    ) -> list[QuoteResponse]:
        """
        Return quotes for multiple symbols.
        """
        raise NotImplementedError