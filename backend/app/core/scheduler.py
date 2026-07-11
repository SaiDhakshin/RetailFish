from apscheduler.schedulers.background import BackgroundScheduler

from app.core.settings import settings
from app.scheduler.historical_sync_scheduler import (
    HistoricalSyncScheduler,
)

scheduler = BackgroundScheduler()

historical_scheduler = HistoricalSyncScheduler()

if settings.HISTORY_SYNC_ENABLED:

    # scheduler.add_job(
        # func=historical_scheduler.sync_all_daily,
        # trigger="cron",
        # hour=settings.HISTORY_SYNC_HOUR,
        # minute=settings.HISTORY_SYNC_MINUTE,
        # id="daily-history-sync",
        # replace_existing=True,
        # max_instances=1,
        # coalesce=True,
        # misfire_grace_time=3600,
    # )

    scheduler.add_job(
        func=historical_scheduler.sync_all_daily,
        trigger="interval",
        minutes=1000,
        id="daily-history-sync",
        replace_existing=True,
        max_instances=1,
    )