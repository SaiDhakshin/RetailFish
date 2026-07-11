from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class WatchlistItem(Base):
    """
    Instrument belonging to a watchlist.
    """

    __tablename__ = "watchlist_items"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    @property
    def symbol(self) -> str:
        return self.instrument.symbol

    watchlist_id: Mapped[int] = mapped_column(
        ForeignKey(
            "watchlists.id",
            ondelete="CASCADE",
        )
    )

    instrument_id: Mapped[int] = mapped_column(
        ForeignKey(
            "instruments.id",
            ondelete="CASCADE",
        )
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    watchlist = relationship(
        "Watchlist",
        back_populates="items",
    )

    instrument = relationship(
        "Instrument",
        back_populates="watchlist_items",
    )