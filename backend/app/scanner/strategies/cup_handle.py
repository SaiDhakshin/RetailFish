from app.models.ohlcv import OHLCV
from app.scanner.models.scan_context import ScanContext
from app.scanner.models.scan_filter import ScanFilter
from app.scanner.models.scan_detail import ScanDetail
from typing import Any

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

    def overlays(
        self,
        candles: list[OHLCV],
        context: ScanContext,
        indicators: IndicatorCache,
    ) -> list[dict[str, Any]]:
        result = detect_cup_handle(candles)

        if result is None or result.overlay is None:
            return []

        overlay = result.overlay
        cup_points = [
            {
                "time": point["time"],
                "value": point["price"],
            }
            for point in overlay["cup"]
        ]
        handle_points = [
            {
                "time": point["time"],
                "value": point["price"],
            }
            for point in overlay["handle"]
        ]
        breakout_price = overlay["breakout_price"]
        label_point = {
            "time": overlay["label"]["time"],
            "value": overlay["label"]["price"],
        }

        return [
            {
                "id": f"cup_handle_cup_{label_point['time']}_{label_point['value']}",
                "type": "polyline",
                "color": "#71b3ff",
                "points": cup_points,
            },
            {
                "id": f"cup_handle_handle_{label_point['time']}_{label_point['value']}",
                "type": "polyline",
                "color": "#84e472",
                "points": handle_points,
            },
            {
                "id": f"cup_handle_breakout_{label_point['time']}_{breakout_price}",
                "type": "horizontalLine",
                "color": "#f5c542",
                "points": [
                    {
                        "time": cup_points[0]["time"],
                        "value": breakout_price,
                    },
                    {
                        "time": cup_points[-1]["time"],
                        "value": breakout_price,
                    },
                ],
                "text": "Breakout",
            },
            {
                "id": f"cup_handle_label_{label_point['time']}_{label_point['value']}",
                "type": "label",
                "color": "#f2f2f2",
                "points": [label_point],
                "text": overlay["label"]["text"],
            },
        ]
