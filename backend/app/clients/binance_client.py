import httpx

from app.clients.market_data_provider import MarketDataProvider

from app.core.config import BINANCE_BASE_URL, REQUEST_TIMEOUT
from datetime import datetime, UTC

from app.dto.market_data import (
    MarketDataDTO,
)

KLINES_ENDPOINT = "/api/v3/klines"

TIMEFRAME_MAP = {
    "1m": "1m",
    "3m": "3m",
    "5m": "5m",
    "15m": "15m",
    "30m": "30m",
    "1h": "1h",
    "2h": "2h",
    "4h": "4h",
    "6h": "6h",
    "8h": "8h",
    "12h": "12h",
    "1d": "1d",
    "3d": "3d",
    "1w": "1w",
    "1M": "1M",
}

class BinanceClient(MarketDataProvider):

    """
    Client responsible for communicating with external market data providers.
    """

    def __init__(self) -> None:
        self.client = httpx.Client(
            base_url=BINANCE_BASE_URL,
            timeout=httpx.Timeout(REQUEST_TIMEOUT),
            headers={
                "Accept": "application/json",
                "User-Agent": "RetailFish/1.0",
            },
        )

    def fetch_historical(
        self,
        symbol: str,
        timeframe: str,
        limit: int = 1000,
    ) -> list[MarketDataDTO]:
        """
        Fetch historical candles from the market data provider.

        Returns:
            List of normalized candle dictionaries.
        """

        endpoint, params = self.build_historical_request(
            symbol=symbol,
            timeframe=timeframe,
            limit=limit,
        )

        raw_candles = self.send_request(
            endpoint,
            params,
        )

        return self.normalize_history(raw_candles)

    def fetch_latest(
        self,
        symbol: str,
        timeframe: str,
    ):
        pass

    def fetch_symbols(self):
        pass

    def get_exchange_timeframe(self, timeframe: str) -> str:
        """
        Convert internal timeframe to exchange timeframe.
        """
        if timeframe not in TIMEFRAME_MAP:
            raise ValueError(f"Unsupported timeframe: {timeframe}")

        return TIMEFRAME_MAP[timeframe]
    
    def build_historical_request(
        self,
        symbol: str,
        timeframe: str,
        limit: int = 1000,
    ) -> tuple[str, dict]:
        """
        Build the endpoint and query parameters for a historical candle request.

        Returns:
        tuple[str, dict]: (endpoint, query_params)
        """
         # Validate symbol
        if not symbol or not symbol.strip():
            raise ValueError("Symbol cannot be empty.")

        symbol = symbol.strip().upper()

        # Validate timeframe
        exchange_timeframe = self.get_exchange_timeframe(timeframe)

        # Validate limit
        if limit < 1 or limit > 1000:
            raise ValueError("Limit must be between 1 and 1000.")

        endpoint = KLINES_ENDPOINT

        params = {
            "symbol": symbol,
            "interval": exchange_timeframe,
            "limit": limit,
        }

        return endpoint, params
    
    def send_request(
        self,
        endpoint: str,
        params: dict,
    ) -> list:
        """
        Send a GET request to the market data provider.

        Args:
            endpoint: API endpoint.
            params: Query parameters.

        Returns:
            Raw JSON response.

        Raises:
            httpx.HTTPStatusError: If the API returns an error.
            httpx.RequestError: If the request cannot be completed.
        """

        response = self.client.get(
            endpoint,
            params=params,
        )

        response.raise_for_status()

        return response.json()
    
    def normalize_candle(self, candle: list) -> dict:
        """
        Convert a Binance kline into the application's standard candle format.
        """

        return {
            "timestamp": datetime.fromtimestamp(candle[0] / 1000, tz=UTC),
            "open": float(candle[1]),
            "high": float(candle[2]),
            "low": float(candle[3]),
            "close": float(candle[4]),
            "volume": float(candle[5]),
        }
    
    def normalize_history(self, candles: list[list]) -> list[MarketDataDTO]:
        """
        Convert multiple Binance candles into the application's standard format.
        """

        return [
            self.normalize_candle(candle)
            for candle in candles
        ]

