from __future__ import annotations

from datetime import datetime, timezone, UTC
from typing import Any

import time

import pandas as pd
import yfinance as yf

from app.core.logger import logger
from app.clients.market_data_provider import MarketDataProvider

from app.scanner.indicators.ema import calculate_ema

from app.schemas.quote import QuoteResponse

from app.dto.market_data import (
    MarketDataDTO,
)

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from app.core.cache import cache
from app.cache.cache_ttl import CacheTTL


class YahooFinanceClient(MarketDataProvider):
    """
    Yahoo Finance implementation of MarketDataProvider.
    """

    @staticmethod
    def historical_ttl(
        timeframe: str,
    ) -> int:

        mapping = {
            "1m": CacheTTL.HISTORICAL_1M,
            "5m": CacheTTL.HISTORICAL_5M,
            "15m": CacheTTL.HISTORICAL_15M,
            "1h": CacheTTL.HISTORICAL_1H,
            "1d": CacheTTL.HISTORICAL_1D,
            "1wk": CacheTTL.HISTORICAL_1W,
        }

        return mapping.get(
            timeframe,
            CacheTTL.HISTORICAL_1D,
        )

    INTERVAL_MAP = {
        "1m": "1m",
        "2m": "2m",
        "5m": "5m",
        "15m": "15m",
        "30m": "30m",
        "60m": "60m",
        "90m": "90m",
        "1h": "60m",
        "1d": "1d",
        "1wk": "1wk",
        "1mo": "1mo",
    }

    PERIOD_MAP = {
        "1m": "7d",
        "2m": "60d",
        "5m": "60d",
        "15m": "60d",
        "30m": "60d",
        "60m": "730d",
        "90m": "60d",
        "1h": "730d",
        "1d": "10y",
        "1wk": "10y",
        "1mo": "max",
    }

    MAX_RETRIES = 3

    def fetch_historical(
        self,
        symbol: str,
        timeframe: str,
        limit: int = 1000,
        start: datetime | None = None,
    ) -> list[MarketDataDTO]:
        
        cache_key = (
            f"history:"
            f"{symbol}:"
            f"{timeframe}:"
            f"{limit}"
        )

        cached = cache.get(cache_key)

        if cached is not None:
            return cached

        interval = self.INTERVAL_MAP.get(timeframe)

        if interval is None:
            raise ValueError(f"Unsupported timeframe: {timeframe}")

        period = self.PERIOD_MAP[timeframe]

        last_error = None

        for attempt in range(self.MAX_RETRIES):

            try:

                df = yf.download(
                    tickers=symbol,
                    period=period,
                    interval=interval,
                    progress=False,
                    auto_adjust=True,
                    threads=False,
                )

                if df.empty:
                    return []
                
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(0)

                df = df.dropna()

                candles = self._normalize(df.tail(limit))

                if start is not None:
                    candles = [
                        candle
                        for candle in candles
                        if candle.timestamp > start
                    ]

                candles = candles[-limit:]

                cache.set(
                    key=cache_key,
                    value=candles,
                    ttl_seconds=self.historical_ttl(
                        timeframe,
                    )
                )

                return candles

            except Exception as exc:
                last_error = exc
                # import traceback

                # traceback.print_exc()
                # raise
                if attempt < self.MAX_RETRIES - 1:
                    time.sleep(2)

        raise RuntimeError(
            f"Unable to download historical data for {symbol}"
        ) from last_error

    def fetch_quote(
        self,
        symbol: str,
    ) -> QuoteResponse:
        """
        Return the latest market quote.
        """

        ticker = yf.Ticker(symbol)

        try:

            info = ticker.fast_info

            price = float(
                info.get(
                    "lastPrice",
                    0,
                )
            )

            previous_close = float(
                info.get(
                    "previousClose",
                    price,
                )
            )

        except Exception:

            info = ticker.info

            price = float(
                info.get(
                    "currentPrice",
                    0,
                )
            )

            previous_close = float(
                info.get(
                    "previousClose",
                    price,
                )
            )

        change = (
            price - previous_close
        )

        change_percent = (
            (change / previous_close) * 100
            if previous_close
            else 0
        )

        return QuoteResponse(
            symbol=symbol,
            price=price,
            previous_close=previous_close,
            change=round(change, 2),
            change_percent=round(
                change_percent,
                2,
            ),
            currency="INR",
            exchange="NSE",
            timestamp=datetime.now(UTC),
        )

    def fetch_quotes(
        self,
        symbols: list[str],
    ) -> list[QuoteResponse]:
        """
        Return quotes for multiple symbols.
        """

        quotes: list[QuoteResponse] = []

        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = {
                executor.submit(
                    self.fetch_quote,
                    symbol,
                ): symbol
                for symbol in symbols
            }

            for future in as_completed(futures):
                symbol = futures[future]

                try:
                    quotes.append(
                        future.result()
                    )
                except Exception:
                    logger.exception(
                        "Failed quote for %s",
                        symbol,
                    )

        return quotes

    def _normalize(
        self,
        dataframe: pd.DataFrame,
    ) -> list[MarketDataDTO]:

        candles: list[MarketDataDTO] = []

        for timestamp, row in dataframe.iterrows():

            candles.append(
                MarketDataDTO(
                    timestamp=self._convert_timestamp(timestamp),
                    open=float(row.Open),
                    high=float(row.High),
                    low=float(row.Low),
                    close=float(row.Close),
                    volume=float(row.Volume),
                )
            )

        return candles

    @staticmethod
    def _convert_timestamp(value: datetime | pd.Timestamp) -> datetime:
        """
        Convert pandas timestamps into timezone-aware UTC datetimes.
        """

        if isinstance(value, pd.Timestamp):
            value = value.to_pydatetime()

        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        else:
            value = value.astimezone(timezone.utc)

        return value