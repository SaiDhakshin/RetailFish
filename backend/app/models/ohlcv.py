from datetime import datetime

from sqlalchemy import (
    ForeignKey,
    Numeric,
    String,
    DateTime,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class OHLCV(Base):
    __tablename__ = "ohlcv"

    __table_args__ = (
        UniqueConstraint(
            "instrument_id",
            "timeframe",
            "timestamp",
            name="uq_ohlcv_candle",
        ),
        Index(
            "idx_ohlcv_lookup",
            "instrument_id",
            "timeframe",
            "timestamp",
        ),
    )

    instrument: Mapped["Instrument"] = relationship(
        "Instrument",
        back_populates="candles",
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    instrument_id: Mapped[int] = mapped_column(
        ForeignKey("instruments.id", ondelete="CASCADE"),
        nullable=False,
    )

    timeframe: Mapped[str] = mapped_column(String(10), nullable=False)

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    open: Mapped[float] = mapped_column(Numeric(18, 8))
    high: Mapped[float] = mapped_column(Numeric(18, 8))
    low: Mapped[float] = mapped_column(Numeric(18, 8))
    close: Mapped[float] = mapped_column(Numeric(18, 8))
    volume: Mapped[float] = mapped_column(Numeric(20, 8))