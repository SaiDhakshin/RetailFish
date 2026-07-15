from app.scanner.models.scan import Scan


class CacheKeys:

    @staticmethod
    def historical(
        symbol: str,
        timeframe: str,
        limit: int,
    ) -> str:

        return (
            f"history:"
            f"{symbol}:"
            f"{timeframe}:"
            f"{limit}"
        )

    @staticmethod
    def scanner(
        scan: Scan,
        timeframe: str,
    ) -> str:

        filters = ",".join(
            sorted(
                filter.value
                for filter in scan.filters
            )
        )

        return (
            f"scanner:"
            f"{scan.universe.value}:"
            f"{timeframe}:"
            f"{filters}"
        )

    @staticmethod
    def quote(
        symbol: str,
    ) -> str:

        return f"quote:{symbol}"