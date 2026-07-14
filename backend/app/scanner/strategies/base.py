from abc import ABC, abstractmethod

from app.models.ohlcv import OHLCV

from app.scanner.models.scan_filter import ScanFilter

from app.scanner.models.scan_context import ScanContext

from app.scanner.models.scan_detail import (
    ScanDetail,
)
from app.scanner.models.indicator_cache import IndicatorCache


class ScannerStrategy(ABC):

    @property
    @abstractmethod
    def filter(self) -> ScanFilter:
        ...

    @abstractmethod
    def matches(
        self,
        candles: list[OHLCV],
        context: ScanContext,
        indicators: IndicatorCache,
    ) -> bool:
        ...

    def score(
        self,
        candles,
        context,
        indicators: IndicatorCache,
    ) -> float:

        return 20
    
    def detail(
        self,
        candles,
        context,
        indicators: IndicatorCache,
    ) -> ScanDetail:

        return ScanDetail(
            filter=self.filter.value,
            value="Matched",
        )