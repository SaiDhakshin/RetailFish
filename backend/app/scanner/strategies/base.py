from abc import ABC, abstractmethod

from app.models.ohlcv import OHLCV

from app.scanner.models.scan_filter import ScanFilter


class ScannerStrategy(ABC):

    @property
    @abstractmethod
    def filter(self) -> ScanFilter:
        ...

    @abstractmethod
    def matches(
        self,
        candles: list[OHLCV],
    ) -> bool:
        ...