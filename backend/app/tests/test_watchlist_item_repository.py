from app.core.database import SessionLocal

from app.models.watchlist_item import WatchlistItem

from app.repositories.instrument_repository import InstrumentRepository
from app.repositories.watchlist_item_repository import (
    WatchlistItemRepository,
)
from app.repositories.watchlist_repository import (
    WatchlistRepository,
)

db = SessionLocal()

try:

    watchlists = WatchlistRepository(db)
    items = WatchlistItemRepository(db)
    instruments = InstrumentRepository(db)

    watchlist = watchlists.get_by_name("Swing")

    instrument = instruments.get_by_symbol(
        "RELIANCE.NS"
    )

    item = WatchlistItem(
        watchlist_id=watchlist.id,
        instrument_id=instrument.id,
    )

    items.create(item)

    print(
        items.get_all(
            watchlist.id,
        )
    )

finally:

    db.close()