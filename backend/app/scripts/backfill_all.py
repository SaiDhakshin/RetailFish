from app.clients.yahoo_finance_client import YahooFinanceClient
from app.core.database import SessionLocal
from app.repositories.instrument_repository import InstrumentRepository
from app.services.market_data_service import MarketDataService


def main():
    db = SessionLocal()

    try:
        service = MarketDataService(
            db=db,
            provider=YahooFinanceClient(),
        )

        repository = InstrumentRepository(db)

        instruments = repository.get_all()

        total = len(instruments)

        print(f"Found {total} instruments")

        for index, instrument in enumerate(instruments, start=1):
            print(
                f"[{index}/{total}] {instrument.symbol}"
            )

            try:
                service.backfill(
                    instrument=instrument,
                    timeframe="1d",
                    limit=1000,
                )

            except Exception as e:
                print(
                    f"Failed {instrument.symbol}: {e}"
                )

        print("Backfill complete")

    finally:
        db.close()


if __name__ == "__main__":
    main()

# docker compose exec backend python -m app.scripts.backfill_all