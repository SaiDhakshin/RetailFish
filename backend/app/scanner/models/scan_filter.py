from enum import Enum


class ScanFilter(str, Enum):
    EMA_ALIGNMENT = "ema_alignment"

    FIFTY_TWO_WEEK_HIGH = "fifty_two_week_high"

    VOLUME_BREAKOUT = "volume_breakout"

    RELATIVE_STRENGTH = "relative_strength"

    CUP_HANDLE = "cup_handle"

    VCP = "vcp"

    TREND_TEMPLATE = "trend_template"