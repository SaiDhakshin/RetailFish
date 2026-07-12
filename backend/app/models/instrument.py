from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

from sqlalchemy.orm import relationship


class Instrument(Base):
    __tablename__ = "instruments"

    candles = relationship(
        "OHLCV",
        back_populates="instrument",
        cascade="all, delete-orphan",
    )

    watchlist_items = relationship(
        "WatchlistItem",
        back_populates="instrument",
        cascade="all, delete-orphan",
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    exchange: Mapped[str | None] = mapped_column(String(20),nullable=False)
    name: Mapped[str | None] = mapped_column(String(100),nullable=False)
    sector: Mapped[str | None] = mapped_column(String(100),nullable=True)
    industry: Mapped[str | None] = mapped_column(String(100),nullable=True)

