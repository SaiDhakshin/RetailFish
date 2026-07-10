from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.ohlcv import OHLCV

from app.models.instrument import Instrument

from sqlalchemy.dialects.postgresql import insert

from sqlalchemy import func


class OHLCVRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, candle: OHLCV) -> OHLCV:
        """
        Save a single OHLCV candle.
        """
        try:
            self.db.add(candle)
            self.db.commit()
            self.db.refresh(candle)
            return candle
        except Exception:
            self.db.rollback()
            raise

    def save_bulk(self, candles: list[OHLCV]) -> int:
        """
        Bulk insert candles.

        Existing candles are ignored using
        ON CONFLICT DO NOTHING.

        Returns:
            Number of newly inserted candles.
        """

        if not candles:
            return 0

        values = [
            {
                "instrument_id": candle.instrument_id,
                "timeframe": candle.timeframe,
                "timestamp": candle.timestamp,
                "open": candle.open,
                "high": candle.high,
                "low": candle.low,
                "close": candle.close,
                "volume": candle.volume,
            }
            for candle in candles
        ]

        stmt = (
            insert(OHLCV)
            .values(values)
            .on_conflict_do_nothing(
                index_elements=[
                    "instrument_id",
                    "timeframe",
                    "timestamp",
                ]
            )
            .returning(OHLCV.id)
        )

        try:
            result = self.db.execute(stmt)

            inserted = len(result.scalars().all())

            self.db.commit()

            return inserted

        except Exception:
            self.db.rollback()
            raise

    def get_history(
        self,
        instrument_id: int,
        timeframe: str,
        start_time: datetime,
        end_time: datetime,
    ) -> list[OHLCV]:
        """
        Fetch historical candles ordered by timestamp.
        """
        stmt = (
            select(OHLCV)
            .where(OHLCV.instrument_id == instrument_id)
            .where(OHLCV.timeframe == timeframe)
            .where(OHLCV.timestamp >= start_time)
            .where(OHLCV.timestamp <= end_time)
            .order_by(OHLCV.timestamp.asc())
        )

        return list(self.db.scalars(stmt).all())

    def latest_timestamp(
        self,
        instrument_id: int,
        timeframe: str,
    ) -> datetime | None:
        """
        Return latest stored candle timestamp.
        """
        stmt = (
            select(OHLCV.timestamp)
            .where(OHLCV.instrument_id == instrument_id)
            .where(OHLCV.timeframe == timeframe)
            .order_by(OHLCV.timestamp.desc())
            .limit(1)
        )

        return self.db.scalar(stmt)

    def exists(
        self,
        instrument_id: int,
        timeframe: str,
        timestamp: datetime,
    ) -> bool:
        """
        Check whether a candle already exists.
        """
        stmt = (
            select(OHLCV.id)
            .where(OHLCV.instrument_id == instrument_id)
            .where(OHLCV.timeframe == timeframe)
            .where(OHLCV.timestamp == timestamp)
            .limit(1)
        )

        return self.db.scalar(stmt) is not None

    def delete_range(
        self,
        instrument_id: int,
        timeframe: str,
        start_time: datetime,
        end_time: datetime,
    ) -> int:
        """
        Delete candles within a time range.
        Returns number of deleted rows.
        """
        try:
            rows = (
                self.db.query(OHLCV)
                .filter(
                    OHLCV.instrument_id == instrument_id,
                    OHLCV.timeframe == timeframe,
                    OHLCV.timestamp >= start_time,
                    OHLCV.timestamp <= end_time,
                )
                .delete(synchronize_session=False)
            )

            self.db.commit()
            return rows

        except Exception:
            self.db.rollback()
            raise

    def get_candles(
        self,
        instrument_id: int,
        timeframe: str,
        limit: int = 500,
    ) -> list[OHLCV]:
        """
        Return historical candles ordered by timestamp.
        """

        stmt = (
            select(OHLCV)
            .where(
                OHLCV.instrument_id == instrument_id,
                OHLCV.timeframe == timeframe,
            )
            .order_by(OHLCV.timestamp.asc())
            .limit(limit)
        )

        return list(
            self.db.scalars(stmt).all()
        )

    def get_latest_timestamp(
        self,
        instrument_id: int,
        timeframe: str,
    ):
        """
        Return the latest stored candle timestamp.
        """

        stmt = (
            select(
                func.max(OHLCV.timestamp)
            )
            .where(
                OHLCV.instrument_id == instrument_id,
                OHLCV.timeframe == timeframe,
            )
        )

        return self.db.scalar(stmt)