from dataclasses import dataclass
from typing import Any

from app.models.ohlcv import OHLCV
from app.scanner.constants import CUP_HANDLE_PIVOT_LOOKBACK, CUP_HANDLE_PIVOT_THRESHOLD


@dataclass(slots=True)
class Pivot:
    index: int
    price: float
    type: str


def _to_float(value: Any) -> float:
    return float(value)


def detect_pivots(
    candles: list[OHLCV],
    lookback: int = CUP_HANDLE_PIVOT_LOOKBACK,
) -> list[Pivot]:
    if len(candles) < lookback * 2 + 1:
        return []

    highs = [_to_float(c.high) for c in candles]
    lows = [_to_float(c.low) for c in candles]
    pivots: list[Pivot] = []

    for index in range(lookback, len(candles) - lookback):
        window_highs = highs[index - lookback: index + lookback + 1]
        window_lows = lows[index - lookback: index + lookback + 1]
        current_high = highs[index]
        current_low = lows[index]

        if (
            current_high == max(window_highs)
            and window_highs.count(current_high) == 1
            and current_high >= max(
                window_highs[:lookback] + window_highs[lookback + 1:],
                default=current_high,
            )
            * (1 + CUP_HANDLE_PIVOT_THRESHOLD)
        ):
            pivots.append(Pivot(index=index, price=current_high, type="high"))

        if (
            current_low == min(window_lows)
            and window_lows.count(current_low) == 1
            and current_low <= min(
                window_lows[:lookback] + window_lows[lookback + 1:],
                default=current_low,
            )
            * (1 - CUP_HANDLE_PIVOT_THRESHOLD)
        ):
            pivots.append(Pivot(index=index, price=current_low, type="low"))

    return sorted(pivots, key=lambda pivot: pivot.index)
