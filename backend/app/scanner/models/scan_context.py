from dataclasses import dataclass

from app.models.ohlcv import OHLCV
from app.scanner.models.indicator_cache import IndicatorCache

@dataclass
class ScanContext:
    benchmark_candles: list[OHLCV]

    indicators: IndicatorCache