from dataclasses import dataclass
from datetime import datetime
from typing import Literal

ChartOverlayType = Literal[
    "polyline",
    "horizontalLine",
    "label",
    "marker",
]


@dataclass(slots=True)
class ChartPoint:
    time: datetime
    value: float


@dataclass(slots=True)
class ChartOverlay:
    id: str
    type: ChartOverlayType
    color: str
    points: list[ChartPoint]
    text: str | None = None
