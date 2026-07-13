from app.models.ohlcv import OHLCV

from app.scanner.models.scan_filter import ScanFilter
from app.scanner.strategies.base import ScannerStrategy


class FiftyTwoWeekHighStrategy(ScannerStrategy):

    @property
    def filter(self) -> ScanFilter:
        return ScanFilter.FIFTY_TWO_WEEK_HIGH

    def matches(
        self,
        candles: list[OHLCV],
    ) -> bool:


        print("Candles:", len(candles))
        if len(candles) < 252:
            return False

        highest_high = max(
            float(candle.high)
            for candle in candles[-252:]
        )

        last_close = float(
            candles[-1].close
        )

        return (
            last_close >= highest_high * 0.98
        )