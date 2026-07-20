from app.models.ohlcv import OHLCV
from app.scanner.models.scan_context import ScanContext
from app.scanner.models.scan_filter import ScanFilter
from app.scanner.models.scan_detail import ScanDetail
from typing import Any

from app.scanner.models.indicator_cache import IndicatorCache
from app.scanner.strategies.base import ScannerStrategy
from app.patterns.vcp import detect_vcp


class VCPStrategy(ScannerStrategy):

    @property
    def filter(self) -> ScanFilter:
        return ScanFilter.VCP

    def matches(
        self,
        candles: list[OHLCV],
        context: ScanContext,
        indicators: IndicatorCache,
    ) -> bool:
        result = detect_vcp(candles)
        return result is not None and result.confidence >= 50

    def score(
        self,
        candles,
        context,
        indicators: IndicatorCache,
    ) -> float:
        result = detect_vcp(candles)
        return float(result.score) if result is not None else 0.0

    def detail(
        self,
        candles,
        context: ScanContext,
        indicators: IndicatorCache,
    ) -> ScanDetail:
        result = detect_vcp(candles)
        if result is None:
            return ScanDetail(filter="VCP", value="No pattern")

        return ScanDetail(
            filter="VCP",
            value=(
                f"Confidence:{result.confidence} "
                f"Breakout:{result.breakout_status}"
            ),
        )

    def overlays(
        self,
        candles: list[OHLCV],
        context: ScanContext,
        indicators: IndicatorCache,
    ) -> list[dict[str, Any]]:
        result = detect_vcp(candles)

        if result is None or result.overlay is None:
            return []

        overlay = result.overlay
        return [
            {
                "id": f"vcp_{result.pattern_type.value}_{result.start_timestamp}",
                "type": "polyline",
                "color": "#f7c948",
                "points": overlay["points"],
            },
        ]
