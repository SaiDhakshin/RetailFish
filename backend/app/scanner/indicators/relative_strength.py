from app.models.ohlcv import OHLCV
from app.scanner.constants import RELATIVE_STRENGTH_PERIOD

def calculate_relative_strength(
    stock: list[OHLCV],
    benchmark: list[OHLCV],
    period: int = RELATIVE_STRENGTH_PERIOD,
) -> float:
    """
    Calculates the stock's performance relative
    to the benchmark.

    Positive values indicate outperformance.
    Negative values indicate underperformance.
    """

    if (
        len(stock) < period
        or len(benchmark) < period
    ):
        return 0.0

    stock_return = (
        float(stock[-1].close)
        / float(stock[-period].close)
    ) - 1

    benchmark_return = (
        float(benchmark[-1].close)
        / float(benchmark[-period].close)
    ) - 1

    return stock_return - benchmark_return