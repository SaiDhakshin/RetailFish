from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.instrument import (
    InstrumentSearchResponse,
)
from app.services.instrument_service import (
    InstrumentService,
)

router = APIRouter(
    prefix="/instruments",
    tags=["Instruments"],
)


@router.get(
    "",
    response_model=InstrumentSearchResponse,
)
def search_instruments(
    q: str = Query(min_length=1),
    limit: int = Query(default=20, le=100),
    db: Session = Depends(get_db),
):

    service = InstrumentService(db)

    return service.search(
        query=q,
        limit=limit,
    )