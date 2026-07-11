from app.core.database import SessionLocal
from app.models.watchlist import Watchlist
from app.repositories.watchlist_repository import WatchlistRepository

db = SessionLocal()

try:

    repo = WatchlistRepository(db)

    watchlist = Watchlist(
        name="Swing",
    )

    repo.create(watchlist)

    print(repo.get_all())

finally:

    db.close()