from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.clients.market_data_provider import MarketDataProvider
from app.core.database import get_db
from app.core.providers import get_market_data_provider
from app.schemas.history import (
    HistoryImportRequest,
    HistoryImportResponse,
)
from app.services.historical_sync_service import HistoricalSyncService
from app.schemas.history_sync import HistorySyncResponse

router = APIRouter(
    prefix="/history",
    tags=["History"],
)


@router.post(
    "/import",
    response_model=HistoryImportResponse,
)
def import_history(
    request: HistoryImportRequest,
    db: Session = Depends(get_db),
    provider: MarketDataProvider = Depends(get_market_data_provider),
):

    service = HistoricalSyncService(
        db=db,
        provider=provider,
    )

    return service.sync(
        symbol=request.symbol,
        timeframe=request.timeframe,
        limit=request.limit,
    )

@router.post(
    "/sync",
    response_model=HistorySyncResponse,
)
def sync_history(
    symbol: str = Query(...),
    timeframe: str = Query(default="1d"),
    db: Session = Depends(get_db),
):
    provider = get_market_data_provider()
    service = HistoricalSyncService(db, provider)

    return service.sync_latest(
        symbol=symbol,
        timeframe=timeframe,
    )