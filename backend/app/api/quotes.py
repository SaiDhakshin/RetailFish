from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.providers import (
    get_market_data_provider,
)
from app.clients.market_data_provider import (
    MarketDataProvider,
)
from app.schemas.quote import QuoteResponse
from app.services.quote_service import QuoteService
from app.schemas.quote import BulkQuoteResponse

router = APIRouter(
    prefix="/quotes",
    tags=["Quotes"],
)


@router.get(
    "",
    response_model=QuoteResponse,
)
def get_quote(
    symbol: str,
    db: Session = Depends(get_db),
    provider: MarketDataProvider = Depends(
        get_market_data_provider,
    ),
):

    service = QuoteService(
        db=db,
        provider=provider,
    )

    return service.get_quote(
        symbol=symbol,
    )

@router.get(
    "/bulk",
    response_model=BulkQuoteResponse,
)
def get_quotes(
    symbols: str,
    db: Session = Depends(get_db),
    provider: MarketDataProvider = Depends(
        get_market_data_provider,
    ),
):

    service = QuoteService(
        db=db,
        provider=provider,
    )

    symbol_list = [
        symbol.strip()
        for symbol in symbols.split(",")
        if symbol.strip()
    ]

    quotes = service.get_quotes(
        symbol_list,
    )

    return BulkQuoteResponse(
        quotes=quotes,
    )