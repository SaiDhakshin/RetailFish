from sqlalchemy.orm import Session

from app.models.watchlist import Watchlist
from app.models.watchlist_item import WatchlistItem

from app.repositories.instrument_repository import InstrumentRepository
from app.repositories.watchlist_item_repository import (
    WatchlistItemRepository,
)
from app.repositories.watchlist_repository import (
    WatchlistRepository,
)

from app.exceptions.watchlist import (
    InstrumentAlreadyInWatchlistError,
    WatchlistNotFoundError,
)


class WatchlistService:
    """
    Business logic for watchlists.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        self.watchlists = WatchlistRepository(db)
        self.items = WatchlistItemRepository(db)
        self.instruments = InstrumentRepository(db)

    # --------------------------------------------------
    # Watchlists
    # --------------------------------------------------

    def list_watchlists(
        self,
    ) -> list[Watchlist]:

        return self.watchlists.get_all()

    def create_watchlist(
        self,
        name: str,
    ) -> Watchlist:

        existing = self.watchlists.get_by_name(name)

        if existing:
            raise ValueError(
                "Watchlist already exists."
            )

        watchlist = Watchlist(
            name=name,
        )

        return self.watchlists.create(
            watchlist,
        )

    def rename_watchlist(
        self,
        watchlist_id: int,
        name: str,
    ) -> Watchlist:

        watchlist = self.watchlists.get_by_id(
            watchlist_id,
        )

        if watchlist is None:
            raise ValueError(
                "Watchlist not found."
            )

        watchlist.name = name

        return self.watchlists.update(
            watchlist,
        )

    def delete_watchlist(
        self,
        watchlist_id: int,
    ) -> None:

        watchlist = self.watchlists.get_by_id(
            watchlist_id,
        )

        if watchlist is None:
            raise ValueError(
                "Watchlist not found."
            )

        self.watchlists.delete(
            watchlist,
        )

    # --------------------------------------------------
    # Items
    # --------------------------------------------------

    def list_items(
        self,
        watchlist_id: int,
    ) -> list[WatchlistItem]:

        return self.items.get_all(
            watchlist_id,
        )

    def add_symbol(
        self,
        watchlist_id: int,
        symbol: str,
    ) -> WatchlistItem:

        watchlist = self.watchlists.get_by_id(
            watchlist_id,
        )

        if watchlist is None:
            raise WatchlistNotFoundError(
                watchlist_id,
            )

        instrument = self.instruments.get_by_symbol(
            symbol,
        )

        if instrument is None:
            raise ValueError(
                f"{symbol} not found."
            )

        existing = self.items.get(
            watchlist_id,
            instrument.id,
        )

        if existing:
            raise InstrumentAlreadyInWatchlistError(
                symbol,
            )

        item = WatchlistItem(
            watchlist_id=watchlist_id,
            instrument_id=instrument.id,
        )

        return self.items.create(
            item,
        )

    def remove_symbol(
        self,
        watchlist_id: int,
        instrument_id: int,
    ) -> None:

        item = self.items.get(
            watchlist_id,
            instrument_id,
        )

        if item is None:
            return

        self.items.delete(
            item,
        )