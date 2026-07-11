from sqlalchemy.orm import Session

from app.clients.market_data_provider import (
    MarketDataProvider,
)
from app.repositories.instrument_repository import (
    InstrumentRepository,
)
from app.schemas.quote import QuoteResponse

from app.exceptions.instrument import (
    InstrumentNotFoundError,
)


class QuoteService:
    """
    Service responsible for retrieving
    live market quotes.
    """

    def __init__(
        self,
        db: Session,
        provider: MarketDataProvider,
    ) -> None:

        self.provider = provider

        self.instrument_repository = (
            InstrumentRepository(db)
        )

    def get_quote(
        self,
        symbol: str,
    ) -> QuoteResponse:
        """
        Return the latest market quote.
        """

        instrument = (
            self.instrument_repository.get_by_symbol(
                symbol,
            )
        )

        if instrument is None:
            raise InstrumentNotFoundError(
                symbol,
            )

        return self.provider.fetch_quote(
            symbol=symbol,
        )
    
    def get_quotes(
        self,
        symbols: list[str],
    ) -> list[QuoteResponse]:
        """
        Return quotes for multiple symbols.
        """

        return self.provider.fetch_quotes(
            symbols,
        )