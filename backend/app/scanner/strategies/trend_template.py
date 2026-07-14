from app.models.ohlcv import OHLCV

from app.scanner.models.scan_context import ScanContext
from app.scanner.models.indicator_cache import IndicatorCache
from app.scanner.models.scan_detail import ScanDetail
from app.scanner.models.scan_filter import ScanFilter
from app.scanner.constants import (
    TREND_TEMPLATE_MAX_DISTANCE_FROM_HIGH,
)

from app.scanner.strategies.base import ScannerStrategy


class TrendTemplateStrategy(
    ScannerStrategy,
):

    @property
    def filter(self):
        return ScanFilter.TREND_TEMPLATE

    def matches(
        self,
        candles: list[OHLCV],
        context: ScanContext,
        indicators: IndicatorCache,
    ) -> bool:

        last = float(candles[-1].close)

        return (
            last > indicators.ema20
            and indicators.ema20 > indicators.ema50
            and indicators.ema50 > indicators.ema200
            and indicators.relative_strength > 0
            and last >= (
                indicators.fifty_two_week_high
                * TREND_TEMPLATE_MAX_DISTANCE_FROM_HIGH
            )
        )

    def score(
        self,
        candles,
        context,
        indicators,
    ) -> float:

        return 50

    def detail(
        self,
        candles,
        context,
        indicators,
    ) -> ScanDetail:

        return ScanDetail(
            filter="Trend Template",
            value="Minervini Passed",
        )