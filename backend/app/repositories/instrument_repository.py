from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.models.instrument import Instrument


class InstrumentRepository:
    """
    Repository for Instrument operations.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_by_symbol(
        self,
        symbol: str,
    ) -> Instrument | None:
        """
        Return an instrument by symbol.
        """

        stmt = (
            select(Instrument)
            .where(Instrument.symbol == symbol)
        )

        return self.db.scalar(stmt)

    def get_all(
        self,
    ):
        stmt = (
            select(Instrument)
            .order_by(
                Instrument.symbol
            )
        )

        return list(
            self.db.scalars(stmt).all()
        )

    def create(
        self,
        symbol: str,
    ) -> Instrument:

        instrument = Instrument(symbol=symbol)

        self.db.add(instrument)
        self.db.commit()
        self.db.refresh(instrument)

        return instrument

    def exists(
        self,
        symbol: str,
    ) -> bool:

        return self.get_by_symbol(symbol) is not None

    def save_bulk(
        self,
        symbols: list[str],
    ) -> int:
        """
        Bulk insert symbols.

        Existing symbols are ignored.
        """

        if not symbols:
            return 0

        values = [
            {
                "symbol": symbol,
            }
            for symbol in symbols
        ]

        stmt = (
            insert(Instrument)
            .values(values)
            .on_conflict_do_nothing(
                index_elements=["symbol"],
            )
            .returning(Instrument.id)
        )

        result = self.db.execute(stmt)

        inserted = len(result.scalars().all())

        self.db.commit()

        return inserted

    def search(
        self,
        query: str,
        limit: int = 20,
    ) -> list[Instrument]:

        stmt = (
            select(Instrument)
            .where(
                Instrument.symbol.ilike(f"%{query}%")
            )
            .limit(limit)
        )

        return list(self.db.scalars(stmt).all())