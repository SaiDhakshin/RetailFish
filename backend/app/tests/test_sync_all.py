from app.core.database import SessionLocal
from app.services.historical_sync_service import HistoricalSyncService

db = SessionLocal()

try:
    service = HistoricalSyncService(db)

    result = service.sync_all(
        symbols=[
            "BTCUSDT",
        ],
        timeframe="1m",
        limit=10,
    )

    print(result)

finally:
    db.close()