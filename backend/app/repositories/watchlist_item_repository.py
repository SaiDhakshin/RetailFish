from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.watchlist_item import WatchlistItem


class WatchlistItemRepository:
    """
    Repository for watchlist items.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db

    def get_all(
        self,
        watchlist_id: int,
    ) -> list[WatchlistItem]:

        stmt = (
            select(WatchlistItem)
            .options(
                joinedload(
                    WatchlistItem.instrument
                )
            )
            .where(
                WatchlistItem.watchlist_id
                == watchlist_id
            )
            .order_by(
                WatchlistItem.created_at
            )
        )

        return list(
            self.db.scalars(stmt).all()
        )

    def get(
        self,
        watchlist_id: int,
        instrument_id: int,
    ) -> WatchlistItem | None:

        stmt = (
            select(WatchlistItem)
            .where(
                WatchlistItem.watchlist_id
                == watchlist_id,
                WatchlistItem.instrument_id
                == instrument_id,
            )
        )

        return self.db.scalar(stmt)

    def create(
        self,
        item: WatchlistItem,
    ) -> WatchlistItem:

        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)

        return item

    def delete(
        self,
        item: WatchlistItem,
    ) -> None:

        self.db.delete(item)
        self.db.commit()