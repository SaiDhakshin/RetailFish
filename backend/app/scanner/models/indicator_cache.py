from dataclasses import dataclass


@dataclass
class IndicatorCache:

    ema20: float

    ema50: float

    ema200: float

    volume_sma20: float

    fifty_two_week_high: float

    relative_strength: float