from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.schemas.market_data import (
    BackfillRequest,
    BackfillResponse,
)
from app.services.market_data_service import MarketDataService
from app.clients.market_data_provider import MarketDataProvider
from app.core.providers import get_market_data_provider

router = APIRouter(prefix="/market-data", tags=["Market Data"])

@router.post(
    "/backfill",
    response_model=BackfillResponse,
)
def backfill_market_data(
    request: BackfillRequest,
    db: Session = Depends(get_db),
    provider: MarketDataProvider = Depends(get_market_data_provider)
):
    """
    Download historical market data and store it.
    """

    service = MarketDataService(db, provider)

    result = service.backfill(
        symbol=request.symbol,
        timeframe=request.timeframe,
        limit=request.limit,
    )

    return BackfillResponse(**result)