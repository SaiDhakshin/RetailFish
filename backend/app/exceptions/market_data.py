class MarketDataDownloadError(Exception):

    def __init__(self, symbol: str):

        super().__init__(
            f"Unable to download market data for {symbol}."
        )

        self.symbol = symbol