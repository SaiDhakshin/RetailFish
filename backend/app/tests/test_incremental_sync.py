from app.core.database import SessionLocal
from app.services.historical_sync_service import HistoricalSyncService
from app.core.providers import get_market_data_provider

db = SessionLocal()

try:
    provider = get_market_data_provider()
    service = HistoricalSyncService(db,provider)

    result = service.sync_latest(
        symbol="RELIANCE.NS",
        timeframe="1d",
    )

    print(result)

finally:
    db.close()