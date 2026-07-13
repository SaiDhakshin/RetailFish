from app.models.ohlcv import OHLCV


def calculate_sma(
    candles: list[OHLCV],
    period: int,
) -> list[float]:
    """
    Calculates a Simple Moving Average.
    """

    if len(candles) < period:
        return []

    values: list[float] = []

    volumes = [
        float(c.volume)
        for c in candles
    ]

    print(volumes[-5:])

    for i in range(period - 1, len(volumes)):
        window = volumes[
            i - period + 1 : i + 1
        ]

        values.append(
            sum(window) / period
        )

    return values
