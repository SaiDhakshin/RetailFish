from app.models.ohlcv import OHLCV

from app.scanner.indicators.ema import calculate_ema
from app.scanner.models.scan_filter import ScanFilter
from app.scanner.strategies.base import ScannerStrategy


class EMAAlignmentStrategy(ScannerStrategy):

    @property
    def filter(self) -> ScanFilter:
        return ScanFilter.EMA_ALIGNMENT

    def matches(
        self,
        candles: list[OHLCV],
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