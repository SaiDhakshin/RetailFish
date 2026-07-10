from __future__ import annotations

from enum import StrEnum


class TimeFrame(StrEnum):
    ONE_MINUTE = "1m"
    FIVE_MINUTES = "5m"
    FIFTEEN_MINUTES = "15m"
    ONE_HOUR = "1h"
    ONE_DAY = "1d"
    ONE_WEEK = "1wk"
    ONE_MONTH = "1mo"


SUPPORTED_TIMEFRAMES: tuple[str, ...] = (
    TimeFrame.ONE_MINUTE,
    TimeFrame.FIVE_MINUTES,
    TimeFrame.FIFTEEN_MINUTES,
    TimeFrame.ONE_HOUR,
    TimeFrame.ONE_DAY,
    TimeFrame.ONE_WEEK,
    TimeFrame.ONE_MONTH,
)