from app.core.database import SessionLocal
from app.services.watchlist_service import WatchlistService

db = SessionLocal()

try:

    service = WatchlistService(db)

    watchlist = service.create_watchlist(
        "Momentum",
    )

    service.add_symbol(
        watchlist.id,
        "RELIANCE.NS",
    )

    service.add_symbol(
        watchlist.id,
        "TCS.NS",
    )

    items = service.list_items(
        watchlist.id,
    )

    print(items)

finally:

    db.close()