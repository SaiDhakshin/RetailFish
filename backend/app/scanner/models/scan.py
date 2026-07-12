from dataclasses import dataclass

from .scan_filter import ScanFilter
from .scan_universe import ScanUniverse


@dataclass(slots=True)
class Scan:
    universe: ScanUniverse

    filters: list[ScanFilter]