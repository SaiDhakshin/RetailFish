from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any


class PatternType(str, Enum):
    CUP_HANDLE = "cup_handle"


@dataclass(slots=True)
class PatternResult:
    pattern_type: PatternType
    confidence: int
    breakout_price: float
    start_timestamp: datetime
    end_timestamp: datetime
    metadata: dict[str, Any]
    overlay: dict[str, Any] | None = None
