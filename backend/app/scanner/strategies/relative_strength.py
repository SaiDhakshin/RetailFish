from app.models.ohlcv import OHLCV

from app.scanner.indicators.relative_strength import (
    calculate_relative_strength,
)

from app.scanner.models.scan_context import ScanContext
from app.scanner.models.scan_filter import ScanFilter
from app.scanner.strategies.base import ScannerStrategy
from app.scanner.models.scan_detail import ScanDetail


class RelativeStrengthStrategy(ScannerStrategy):

    @property
    def filter(self) -> ScanFilter:
        return ScanFilter.RELATIVE_STRENGTH

    def matches(
        self,
        candles: list[OHLCV],
        context: ScanContext,
        indicators
    ) -> bool:

        rs = calculate_relative_strength(
            stock=candles,
            benchmark=context.benchmark_candles,
        )

        print(
            candles[-1].close,
            rs,
        )

        return rs > 0
    
    def score(
        self,
        candles,
        context,
        indicators
    ) -> float:

        rs = calculate_relative_strength(
            stock=candles,
            benchmark=context.benchmark_candles,
        )

        if rs <= 0:
            return 0

        return min(
            rs * 100,
            40,
        )
    
    def detail(
        self,
        candles,
        context,
        indicators
    ) -> ScanDetail:

        rs = calculate_relative_strength(
            candles,
            context.benchmark_candles,
        )

        return ScanDetail(
            filter="Relative Strength",
            value=f"{rs:.1%}",
        )