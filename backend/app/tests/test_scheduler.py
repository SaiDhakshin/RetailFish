from app.core.database import SessionLocal
from app.scheduler.historical_sync_scheduler import (
    HistoricalSyncScheduler,
)

db = SessionLocal()

try:
    scheduler = HistoricalSyncScheduler(db)

    result = scheduler.run_once(
        symbols=["BTCUSDT"],
        timeframe="1m",
        limit=10,
    )

    print(result)

finally:
    db.close()

# docker compose exec backend python -m app.tests.test_scheduler