from app.core.database import SessionLocal
from app.clients.binance_client import BinanceClient
from app.services.historical_sync_service import HistoricalSyncService

db = SessionLocal()

try:
    provider = BinanceClient()

    service = HistoricalSyncService(
        db=db,
        provider=provider,
    )

    result = service.sync(
        symbol="BTCUSDT",
        timeframe="1m",
        limit=10,
    )

    print(result)

finally:
    db.close()