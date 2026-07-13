from collections.abc import Iterable

from app.models.instrument import Instrument

from app.scanner.models.scan import Scan
from app.scanner.models.scan_result import ScanResult
from app.scanner.repository.market_data_repository import (
    MarketDataRepository,
)
from app.scanner.strategies.base import ScannerStrategy
from app.scanner.scoring import FILTER_SCORES


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

        for instrument in instruments:

            candles = self._repository.get_candles(
                instrument.id,
                timeframe,
                candle_limit,
            )

            if not candles:
                continue

            matched_filters: list[str] = []

            score = 0

            for filter_type in scan.filters:

                strategy = self._strategies.get(filter_type)

                if strategy is None:
                    continue

                if strategy.matches(candles):

                    matched_filters.append(
                        filter_type.value,
                    )

                    score += FILTER_SCORES[filter_type]

            if not matched_filters:
                continue

            results.append(
                ScanResult(
                    symbol=instrument.symbol,
                    score=score,
                    matched_filters=matched_filters,
                )
            )

        results.sort(
            key=lambda result: result.score,
            reverse=True,
        )

        return results