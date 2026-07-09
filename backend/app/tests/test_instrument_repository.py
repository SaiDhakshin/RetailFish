from app.core.database import SessionLocal
from app.repositories.instrument_repository import InstrumentRepository

db = SessionLocal()

try:

    repository = InstrumentRepository(db)

    inserted = repository.save_bulk(
        [
            "RELIANCE.NS",
            "TCS.NS",
            "INFY.NS",
        ]
    )

    print("Inserted:", inserted)

    print(repository.exists("RELIANCE.NS"))

    print(repository.search("RELI"))

finally:
    db.close()

# docker compose exec backend python -m app.tests.test_instrument_repository