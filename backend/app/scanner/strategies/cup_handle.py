from app.models.ohlcv import OHLCV
from app.scanner.models.scan_context import ScanContext
from app.scanner.models.scan_filter import ScanFilter
from app.scanner.models.scan_detail import ScanDetail
from app.scanner.models.indicator_cache import IndicatorCache
from app.scanner.strategies.base import ScannerStrategy
from app.scanner.utils.cup_handle import detect_cup_handle


class CupHandleStrategy(ScannerStrategy):

    @property
    def filter(self) -> ScanFilter:
        return ScanFilter.CUP_HANDLE

    def matches(
        self,
        candles: list[OHLCV],
        context: ScanContext,
        indicators: IndicatorCache,
    ) -> bool:
        result = detect_cup_handle(candles)
        return result is not None and result.confidence >= 50

    def score(
        self,
        candles,
        context,
        indicators: IndicatorCache,
    ) -> float:
        result = detect_cup_handle(candles)
        return float(result.confidence) if result is not None else 0.0

    def detail(
        self,
        candles,
        context: ScanContext,
        indicators: IndicatorCache,
    ) -> ScanDetail:
        result = detect_cup_handle(candles)
        if result is None:
            return ScanDetail(filter="Cup Handle", value="No pattern")

        metadata = result.metadata
        value = (
            f"Conf:{result.confidence} "
            f"Depth:{metadata['cup_depth']:.1%} "
            f"Hdl:{metadata['handle_depth']:.1%} "
            f"Dur:{metadata['cup_duration']}+{metadata['handle_duration']}"
        )

        return ScanDetail(
            filter="Cup Handle",
            value=value,
        )
