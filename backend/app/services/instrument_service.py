from sqlalchemy.orm import Session

from app.repositories.instrument_repository import (
    InstrumentRepository,
)


class InstrumentService:
    """
    Business logic for instruments.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        self.repository = InstrumentRepository(db)

    def search(
        self,
        query: str,
        limit: int = 20,
    ) -> dict:

        instruments = self.repository.search(
            query=query,
            limit=limit,
        )

        return {
            "total": len(instruments),
            "items": instruments,
        }