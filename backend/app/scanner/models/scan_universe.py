from enum import Enum


class ScanUniverse(str, Enum):
    NIFTY50 = "nifty50"

    NIFTY100 = "nifty100"

    NIFTY200 = "nifty200"

    NIFTY500 = "nifty500"

    ALL = "all"