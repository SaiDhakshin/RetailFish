from app.models.ohlcv import OHLCV


def calculate_ema(
    candles: list[OHLCV],
    period: int,
) -> list[float]:
    """
    Calculates Exponential Moving Average.

    Returns one EMA value per candle.
    """

    if not candles:
        return []

    multiplier = 2 / (period + 1)

    ema_values: list[float] = []

    ema = float(candles[0].close)

    ema_values.append(ema)

    for candle in candles[1:]:
        ema = (
            (float(candle.close) - ema) * multiplier
        ) + ema

        ema_values.append(ema)

    return ema_values