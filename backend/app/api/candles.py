from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.candle import CandleResponse
from app.services.candle_service import CandleService

from fastapi import HTTPException
from app.core.timeframes import SUPPORTED_TIMEFRAMES

from app.core.timeframes import TimeFrame

router = APIRouter(
    prefix="/candles",
    tags=["Candles"],
)


@router.get(
    "",
    response_model=list[CandleResponse],
)
def get_candles(
    symbol: str,
    timeframe: TimeFrame = Query(default=TimeFrame.ONE_DAY),
    limit: int = Query(default=1000, le=5000),
    db: Session = Depends(get_db),
):

    service = CandleService(db)

    return service.get_candles(
        symbol,
        timeframe,
        limit,
    )