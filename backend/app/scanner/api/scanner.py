from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.scanner.schemas.scan_request import ScanRequest
from app.scanner.schemas.scan_response import ScanResponse

from app.scanner.models.scan import Scan

from app.scanner.repository.market_data_repository import (
    MarketDataRepository,
)

from app.scanner.services.scanner_service import ScannerService

from app.scanner.strategies.ema_alignment import (
    EMAAlignmentStrategy,
)

from app.scanner.strategies.volume_breakout import (
    VolumeBreakoutStrategy,
)

from app.scanner.strategies.fifty_two_week_high import (
    FiftyTwoWeekHighStrategy,
)

router = APIRouter(
    prefix="/scanner",
    tags=["Scanner"],
)


@router.post(
    "/run",
    response_model=list[ScanResponse],
)
def run_scan(
    request: ScanRequest,
    db: Session = Depends(get_db),
) -> list[ScanResponse]:

    repository = MarketDataRepository(db)

    service = ScannerService(
        repository=repository,
        strategies=[
            EMAAlignmentStrategy(),
            VolumeBreakoutStrategy(),
            FiftyTwoWeekHighStrategy(),
        ],
    )

    results = service.run(
        Scan(
            universe=request.universe,
            filters=request.filters,
        )
    )

    return [
        ScanResponse(
            symbol=result.symbol,
            score=result.score,
            matched_filters=result.matched_filters,
        )
        for result in results
    ]