from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, frozen=True)
class MarketDataDTO:
    """
    Standard candle representation shared
    by all market data providers.
    """

    timestamp: datetime

    open: float

    high: float

    low: float

    close: float

    volume: float