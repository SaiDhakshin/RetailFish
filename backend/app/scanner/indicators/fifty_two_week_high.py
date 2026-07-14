from app.models.ohlcv import OHLCV

from app.scanner.constants import (
    FIFTY_TWO_WEEK_PERIOD,
)


def calculate_fifty_two_week_high(
    candles: list[OHLCV],
) -> float:
    """
    Returns the highest closing price over
    the last 52 weeks.
    """

    if len(candles) < FIFTY_TWO_WEEK_PERIOD:
        return 0

    closes = [
        float(c.close)
        for c in candles[-FIFTY_TWO_WEEK_PERIOD:]
    ]

    return max(closes)