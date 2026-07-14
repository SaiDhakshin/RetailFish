from app.models.ohlcv import OHLCV

from app.scanner.indicators.ema import calculate_ema
from app.scanner.models.scan_filter import ScanFilter
from app.scanner.strategies.base import ScannerStrategy
from app.scanner.models.scan_context import ScanContext
from app.scanner.models.scan_detail import (
    ScanDetail,
)
from app.scanner.models.indicator_cache import IndicatorCache


class EMAAlignmentStrategy(ScannerStrategy):

    @property
    def filter(self) -> ScanFilter:
        return ScanFilter.EMA_ALIGNMENT

    def matches(
        self,
        candles: list[OHLCV],
        context: ScanContext,
        indicators: IndicatorCache,
    ) -> bool:

        if len(candles) < 200:
            return False

        ema20 = calculate_ema(candles, 20)
        ema50 = calculate_ema(candles, 50)
        ema200 = calculate_ema(candles, 200)

        return (
            ema20[-1] > ema50[-1]
            and ema50[-1] > ema200[-1]
        )
    
    def detail(
        self,
        candles,
        context,
        indicators: IndicatorCache,
    ) -> ScanDetail:

        return ScanDetail(
            filter="EMA Alignment",
            value="20 > 50 > 200",
        )