class InstrumentNotFoundError(Exception):

    def __init__(self, symbol: str):

        super().__init__(
            f"Instrument '{symbol}' not found."
        )

        self.symbol = symbol