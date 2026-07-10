from collections.abc import Generator

from sqlalchemy.orm import Session

from app.core.database import SessionLocal

from app.clients.market_data_provider import MarketDataProvider
from app.core.providers import get_market_data_provider
from app.repositories.instrument_repository import InstrumentRepository
from app.repositories.ohlcv_repository import OHLCVRepository
from app.services.market_data_service import MarketDataService



def get_db() -> Generator[Session, None, None]:
    """
    Create a database session for each request.
    """

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

def get_market_data_service(
    db: Session,
) -> MarketDataService:

    return MarketDataService(
        instrument_repository=InstrumentRepository(db),
        ohlcv_repository=OHLCVRepository(db),
        provider=get_market_data_provider(),
    )