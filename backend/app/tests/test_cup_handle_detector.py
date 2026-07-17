from dataclasses import dataclass
from datetime import datetime, timedelta

from app.scanner.utils.cup_handle import detect_cup_handle


@dataclass
class TestCandle:
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


def _build_candle(timestamp, open_price, high, low, close, volume=1_000):
    return TestCandle(
        timestamp=timestamp,
        open=open_price,
        high=high,
        low=low,
        close=close,
        volume=volume,
    )


def test_detect_cup_handle_simple_pattern():
    base = datetime(2026, 1, 1)
    candles = []

    for i, price in enumerate([
        10.0,
        10.5,
        11.0,
        10.6,
        10.2,
        9.8,
        9.6,
        9.7,
        9.9,
        10.2,
        10.7,
        11.0,
        10.8,
        10.6,
        10.7,
        10.9,
        11.1,
    ]):
        candles.append(
            _build_candle(
                timestamp=base + timedelta(days=i),
                open_price=price * 0.99,
                high=price,
                low=price * 0.98,
                close=price * 0.995,
            )
        )

    result = detect_cup_handle(candles)

    assert result is not None
    assert result.pattern_type.value == "cup_handle"
    assert 0 <= result.confidence <= 100
    assert result.breakout_price > 0
    assert result.metadata["cup_depth"] > 0
    assert result.metadata["handle_duration"] >= 3
