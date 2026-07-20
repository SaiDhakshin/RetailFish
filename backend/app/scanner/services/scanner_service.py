from collections.abc import Iterable
from typing import Any

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
from app.core.cache import cache
from app.cache.cache_ttl import CacheTTL

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

        cache_key = (
            f"scanner:"
            f"{scan.universe.value}:"
            f"{timeframe}:"
            f"{','.join(sorted(
                filter.value
                for filter in scan.filters
            ))}"
        )

        cached = cache.get(cache_key)

        if cached is not None:
            return cached

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

            # Temporary debug
            if instrument.symbol == "^NSEI":
                print("Skipping benchmark")
                continue

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

            indicator_cache = IndicatorCache(
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
                indicators=indicator_cache,
            )            

            matched_filters: list[str] = []

            score = 0

            details = []

            overlays: list[dict[str, Any]] = []

            for filter_type in scan.filters:

                strategy = self._strategies.get(filter_type)

                if strategy is None:
                    continue

                matched = strategy.matches(
                    candles,
                    context,
                    indicator_cache,
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
                        indicator_cache,
                    )
                )

                overlays.extend(
                    strategy.overlays(
                        candles,
                        context,
                        indicator_cache,
                    )
                )

                score += strategy.score(
                    candles,
                    context,
                    indicator_cache,
                )

            if not matched_filters:
                continue

            results.append(
                ScanResult(
                    symbol=instrument.symbol,
                    score=score,
                    matched_filters=matched_filters,
                    details=details,
                    relative_strength=indicator_cache.relative_strength,
                    volume_ratio=(
                        float(candles[-1].volume)
                        / indicator_cache.volume_sma20
                        if indicator_cache.volume_sma20 > 0
                        else 0
                    ),

                    distance_from_high=(
                        (
                            float(candles[-1].close)
                            / indicator_cache.fifty_two_week_high
                            - 1
                        )
                        * 100
                        if indicator_cache.fifty_two_week_high > 0
                        else 0
                    ),
                    overlays=overlays,
                )
            )

        results.sort(
            key=lambda result: result.score,
            reverse=True,
        )
        if results:
            print('scanner results:', results[0])
        else:
            print('scanner results: no matches found')

        cache.set(
            key=cache_key,
            value=results,
            ttl_seconds=CacheTTL.SCANNER_RESULTS
        )

        return results