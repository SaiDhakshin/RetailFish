from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.watchlist import Watchlist


class WatchlistRepository:
    """
    Repository for watchlists.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db

    def get_all(
        self,
    ) -> list[Watchlist]:

        stmt = (
            select(Watchlist)
            .order_by(Watchlist.name)
        )

        return list(
            self.db.scalars(stmt).all()
        )

    def get_by_id(
        self,
        watchlist_id: int,
    ) -> Watchlist | None:

        return self.db.get(
            Watchlist,
            watchlist_id,
        )

    def get_by_name(
        self,
        name: str,
    ) -> Watchlist | None:

        stmt = (
            select(Watchlist)
            .where(
                Watchlist.name == name
            )
        )

        return self.db.scalar(stmt)

    def create(
        self,
        watchlist: Watchlist,
    ) -> Watchlist:

        self.db.add(watchlist)
        self.db.commit()
        self.db.refresh(watchlist)

        return watchlist

    def update(
        self,
        watchlist: Watchlist,
    ) -> Watchlist:

        self.db.commit()
        self.db.refresh(watchlist)

        return watchlist

    def delete(
        self,
        watchlist: Watchlist,
    ) -> None:

        self.db.delete(watchlist)
        self.db.commit()