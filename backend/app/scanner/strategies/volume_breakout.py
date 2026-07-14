from app.models.ohlcv import OHLCV

from app.scanner.indicators.ema import calculate_ema
from app.scanner.indicators.sma import calculate_sma

from app.scanner.models.scan_filter import ScanFilter

from app.scanner.strategies.base import ScannerStrategy
from app.scanner.models.scan_context import ScanContext
from app.scanner.models.scan_detail import (
    ScanDetail,
)
from app.scanner.models.indicator_cache import IndicatorCache


class VolumeBreakoutStrategy(
    ScannerStrategy,
):

    @property
    def filter(self):
        return ScanFilter.VOLUME_BREAKOUT

    def matches(
        self,
        candles: list[OHLCV],
        context: ScanContext,
        indicators: IndicatorCache,
    ) -> bool:

        if len(candles) < 20:
            return False

        ema20 = calculate_ema(
            candles,
            20,
        )[-1]

        average_volume = indicators.volume_sma20

        last = candles[-1]

        return (
            float(last.close) > ema20
            and float(last.volume)
            > average_volume * 2
        )
    
    def detail(
        self,
        candles,
        context,
        indicators: IndicatorCache,
    ) -> ScanDetail:
        
        average_volume = indicators.volume_sma20

        ratio = (
            float(candles[-1].volume) / average_volume
        )

        return ScanDetail(
            filter="Volume",
            value=f"{ratio:.2f}x Avg20",
        )