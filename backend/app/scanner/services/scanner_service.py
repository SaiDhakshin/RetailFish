from collections.abc import Iterable

from app.models.instrument import Instrument

from app.scanner.models.scan import Scan
from app.scanner.models.scan_result import ScanResult
from app.scanner.repository.market_data_repository import (
    MarketDataRepository,
)

from app.scanner.models.scan_context import ScanContext
from app.repositories.instrument_repository import InstrumentRepository
from app.scanner.strategies.base import ScannerStrategy
from app.scanner.scoring import FILTER_SCORES
from app.scanner.models.indicator_cache import IndicatorCache
from app.scanner.indicators.ema import calculate_ema
from app.scanner.indicators.sma import calculate_sma
from app.scanner.indicators.fifty_two_week_high import calculate_fifty_two_week_high
from app.scanner.constants import MIN_CANDLES_REQUIRED
from app.scanner.indicators.relative_strength import (
    calculate_relative_strength,
)

class ScannerService:
    """
    Coordinates scanner execution.
    """

    def __init__(
        self,
        repository: MarketDataRepository,
        strategies: Iterable[ScannerStrategy],
    ) -> None:
        self._repository = repository

        self._strategies = {
            strategy.filter: strategy
            for strategy in strategies
        }

    def run(
        self,
        scan: Scan,
        timeframe: str = "1d",
        candle_limit: int = 1000,
    ) -> list[ScanResult]:

        results: list[ScanResult] = []

        instruments = self._repository.get_instruments()

        instrument_repository = InstrumentRepository(
            self._repository.db,
        )

        benchmark = instrument_repository.get_by_symbol(
            "^NSEI"
        )

        if benchmark is None:
            raise ValueError("Benchmark not found")

        benchmark_candles = self._repository.get_candles(
            instrument_id=benchmark.id,
            timeframe="1d",
            limit=300,
        )

        for instrument in instruments:

            candles = self._repository.get_candles(
                instrument.id,
                timeframe,
                candle_limit,
            )

            print("Scan running for",
                instrument.symbol,
                len(candles),
            )

            if not candles:
                continue

            if len(candles) < MIN_CANDLES_REQUIRED:
                continue

            cache = IndicatorCache(
                ema20=calculate_ema(
                    candles,
                    20,
                )[-1],
                ema50=calculate_ema(
                    candles,
                    50,
                )[-1],
                ema200=calculate_ema(
                    candles,
                    200,
                )[-1],
                volume_sma20=calculate_sma(
                    candles,
                    20,
                )[-1],
                fifty_two_week_high=calculate_fifty_two_week_high(
                    candles,
                ),
                relative_strength=calculate_relative_strength(
                    candles,
                    benchmark_candles,
                ),
            )

            context = ScanContext(
                benchmark_candles=benchmark_candles,
                indicators=cache,
            )            

            matched_filters: list[str] = []

            score = 0

            details = []

            for filter_type in scan.filters:

                strategy = self._strategies.get(filter_type)

                if strategy is None:
                    continue

                matched = strategy.matches(
                    candles,
                    context,
                    cache,
                )

                if not matched:
                    continue

                matched_filters.append(
                    filter_type.value,
                )

                details.append(
                    strategy.detail(
                        candles,
                        context,
                        cache,
                    )
                )

                score += strategy.score(
                    candles,
                    context,
                    cache,
                )

            if not matched_filters:
                continue

            results.append(
                ScanResult(
                    symbol=instrument.symbol,
                    score=score,
                    matched_filters=matched_filters,
                    details=details,
                )
            )

        results.sort(
            key=lambda result: result.score,
            reverse=True,
        )

        return results