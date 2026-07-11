class WatchlistError(Exception):
    """
    Base exception for watchlists.
    """


class WatchlistNotFoundError(WatchlistError):
    def __init__(self, watchlist_id: int):
        super().__init__(
            f"Watchlist {watchlist_id} not found."
        )


class InstrumentAlreadyInWatchlistError(
    WatchlistError,
):
    def __init__(self, symbol: str):
        super().__init__(
            f"{symbol} already exists in this watchlist."
        )