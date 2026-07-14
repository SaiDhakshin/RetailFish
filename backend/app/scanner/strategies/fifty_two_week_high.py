from app.models.ohlcv import OHLCV

from app.scanner.constants import (
    FIFTY_TWO_WEEK_THRESHOLD,
)

from app.scanner.indicators.fifty_two_week_high import (
    calculate_fifty_two_week_high,
)

from app.scanner.models.scan_context import ScanContext
from app.scanner.models.scan_detail import ScanDetail
from app.scanner.models.scan_filter import ScanFilter
from app.scanner.models.indicator_cache import IndicatorCache
from app.scanner.strategies.base import ScannerStrategy


class FiftyTwoWeekHighStrategy(
    ScannerStrategy,
):

    @property
    def filter(self):
        return ScanFilter.FIFTY_TWO_WEEK_HIGH

    def matches(
        self,
        candles: list[OHLCV],
        context: ScanContext,
        indicators: IndicatorCache,
    ) -> bool:

        high = indicators.fifty_two_week_high

        if high == 0:
            return False

        current = float(
            candles[-1].close
        )

        return (
            current >= high * FIFTY_TWO_WEEK_THRESHOLD
        )

    def score(
        self,
        candles,
        context,
        indicators,
    ) -> float:

        return 25

    def detail(
        self,
        candles,
        context,
        indicators,
    ) -> ScanDetail:

        high = indicators.fifty_two_week_high

        current = float(
            candles[-1].close
        )

        distance = (
            current / high - 1
        ) * 100

        return ScanDetail(
            filter="52 Week High",
            value=f"{distance:.2f}% from high",
        )