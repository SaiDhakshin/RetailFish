from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any


class PatternType(str, Enum):
    CUP_HANDLE = "cup_handle"
    VCP = "vcp"
    DOUBLE_BOTTOM = "double_bottom"
    DOUBLE_TOP = "double_top"
    HEAD_SHOULDERS = "head_shoulders"
    INVERSE_HEAD_SHOULDERS = "inverse_head_shoulders"
    SYMMETRICAL_TRIANGLE = "symmetrical_triangle"
    ASCENDING_TRIANGLE = "ascending_triangle"
    DESCENDING_TRIANGLE = "descending_triangle"
    FLAG = "flag"
    BEAR_FLAG = "bear_flag"
    HARMONIC = "harmonic"
    TRENDLINE = "trendline"


@dataclass(slots=True)
class PatternResult:
    pattern_type: PatternType
    confidence: int
    score: int
    breakout_price: float
    breakout_status: str | None
    start_timestamp: datetime
    end_timestamp: datetime
    metadata: dict[str, Any]
    overlay: dict[str, Any] | None = None
