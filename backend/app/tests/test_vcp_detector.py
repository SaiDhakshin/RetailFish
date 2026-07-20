from dataclasses import dataclass
from datetime import datetime, timedelta

from app.models.ohlcv import OHLCV
from app.patterns.vcp import detect_vcp


@dataclass(slots=True)
class TestCandle:
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


def _build_candle(timestamp, open_price, high, low, close, volume=1000.0):
    return TestCandle(
        timestamp=timestamp,
        open=open_price,
        high=high,
        low=low,
        close=close,
        volume=volume,
    )


def test_detect_vcp_pattern():
    base = datetime(2026, 1, 1)
    candles = []

    prices = [
        10.0,
        10.4,
        10.1,
        10.3,
        10.0,
        9.8,
        9.9,
        10.1,
        9.9,
        10.0,
        10.15,
        9.95,
        10.05,
        10.12,
        10.07,
        10.09,
        10.22,
        10.18,
        10.25,
        10.30,
        10.40,
    ]

    volumes = [
        1200, 1100, 1050, 1025, 1000, 980, 970, 960, 930, 920,
        900, 890, 880, 870, 860, 850, 840, 830, 820, 810, 800,
    ]

    for i, price in enumerate(prices):
        candles.append(
            _build_candle(
                timestamp=base + timedelta(days=i),
                open_price=price * 0.99,
                high=price,
                low=price * 0.98,
                close=price * 0.995,
                volume=volumes[i],
            )
        )

    result = detect_vcp(candles)

    assert result is not None
    assert result.pattern_type.value == "vcp"
    assert result.confidence >= 50
    assert result.breakout_price > 0
    assert result.breakout_status in {"Breakout", "Near Breakout", "Forming"} or result.breakout_status.startswith("Breakout")
    assert result.metadata["contraction_legs"] >= 3
    assert result.metadata["tightening_score"] > 0
    assert isinstance(result.overlay, dict)
    assert "points" in result.overlay
    assert len(result.overlay["points"]) >= 7


def test_detect_vcp_rejects_non_vcp():
    base = datetime(2026, 1, 1)
    candles = []

    for i in range(14):
        price = 10.0 + i * 0.1
        candles.append(
            _build_candle(
                timestamp=base + timedelta(days=i),
                open_price=price,
                high=price * 1.01,
                low=price * 0.99,
                close=price,
                volume=1000.0,
            )
        )

    result = detect_vcp(candles)
    assert result is None
