from app.core.database import SessionLocal
from app.clients.binance_client import BinanceClient

db = SessionLocal()

try:
    service = BinanceClient(db)

    result = service.backfill(
        symbol="BTCUSDT",
        timeframe="1m",
        limit=10,
    )

    print(result)

finally:
    db.close()