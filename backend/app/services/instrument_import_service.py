from __future__ import annotations

from app.clients.nse_symbol_provider import NSESymbolProvider
from app.repositories.instrument_repository import InstrumentRepository


class InstrumentImportService:
    """
    Imports NSE instruments into the database.
    """

    def __init__(
        self,
        provider: NSESymbolProvider,
        repository: InstrumentRepository,
    ) -> None:

        self.provider = provider
        self.repository = repository

    def import_all(self) -> dict:
        """
        Download and import all NSE symbols.
        """

        symbols = self.provider.fetch_symbols()

        inserted = self.repository.save_bulk(symbols)

        skipped = len(symbols) - inserted

        return {
            "requested": len(symbols),
            "inserted": inserted,
            "skipped": skipped,
        }