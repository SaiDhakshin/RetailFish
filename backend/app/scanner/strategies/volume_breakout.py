from app.models.ohlcv import OHLCV

from app.scanner.indicators.ema import calculate_ema
from app.scanner.indicators.sma import calculate_sma

from app.scanner.models.scan_filter import ScanFilter

from app.scanner.strategies.base import ScannerStrategy


class VolumeBreakoutStrategy(
    ScannerStrategy,
):

    @property
    def filter(self):
        return ScanFilter.VOLUME_BREAKOUT

    def matches(
        self,
        candles: list[OHLCV],
    ) -> bool:

        if len(candles) < 20:
            return False

        ema20 = calculate_ema(
            candles,
            20,
        )[-1]

        average_volume = calculate_sma(
            candles,
            20,
        )[-1]

        last = candles[-1]

        return (
            float(last.close) > ema20
            and float(last.volume)
            > average_volume * 2
        )