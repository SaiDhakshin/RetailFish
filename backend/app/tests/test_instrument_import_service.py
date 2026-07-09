from app.clients.nse_symbol_provider import NSESymbolProvider
from app.core.database import SessionLocal
from app.repositories.instrument_repository import InstrumentRepository
from app.services.instrument_import_service import (
    InstrumentImportService,
)

db = SessionLocal()

try:

    provider = NSESymbolProvider()

    repository = InstrumentRepository(db)

    service = InstrumentImportService(
        provider=provider,
        repository=repository,
    )

    result = service.import_all()

    print(result)

finally:
    db.close()

# docker compose exec backend python -m app.tests.test_instrument_import_service