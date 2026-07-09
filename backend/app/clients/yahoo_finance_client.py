from __future__ import annotations

from datetime import datetime
from typing import Any

import time

import pandas as pd
import yfinance as yf

from app.clients.market_data_provider import MarketDataProvider


class YahooFinanceClient(MarketDataProvider):
    """
    Yahoo Finance implementation of MarketDataProvider.
    """

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
        limit: int = 500,
    ) -> list[dict[str, Any]]:

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
                    auto_adjust=False,
                    threads=False,
                )

                if df.empty:
                    return []
                
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(0)

                print(df.columns)
                print(df.head())

                df = df.dropna()

                return self._normalize(df.tail(limit))

            except Exception as exc:
                last_error = exc

                if attempt < self.MAX_RETRIES - 1:
                    time.sleep(2)

        raise RuntimeError(
            f"Unable to download historical data for {symbol}"
        ) from last_error

    def _normalize(
        self,
        dataframe: pd.DataFrame,
    ) -> list[dict[str, Any]]:

        candles: list[dict[str, Any]] = []

        for timestamp, row in dataframe.iterrows():

            candles.append(
                {
                    "timestamp": self._convert_timestamp(timestamp),
                    "open": float(row.Open),
                    "high": float(row.High),
                    "low": float(row.Low),
                    "close": float(row.Close),
                    "volume": float(row.Volume),
                }
            )

        return candles

    @staticmethod
    def _convert_timestamp(value: Any) -> datetime:

        if isinstance(value, pd.Timestamp):
            return value.to_pydatetime()

        return value