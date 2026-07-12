from fastapi import FastAPI

from app.api.market_data import router as market_router

from contextlib import asynccontextmanager

from app.core.scheduler import scheduler

from app.api.instruments import (
    router as instrument_router,
)

from app.api.candles import (
    router as candle_router,
)

from app.api.watchlists import (
    router as watchlist_router,
)

from app.api.quotes import (
    router as quote_router,
)

from app.scanner.api.scanner import router as scanner_router

from app.api.history import router as history_router

from app.core.exception_handlers import (
    register_exception_handlers,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifecycle.
    """

    print(">>> Starting scheduler")

    scheduler.start()

    print(">>> Scheduler started")

    try:
        yield

    finally:
        print(">>> Stopping scheduler")
        scheduler.shutdown(wait=False)


app = FastAPI(
    title="Trading OS Backend",
    version="0.2.0",
    lifespan=lifespan,
)

app.include_router(market_router)

app.include_router(instrument_router)

app.include_router(candle_router)

app.include_router(history_router)

app.include_router(watchlist_router)

app.include_router(quote_router)

app.include_router(scanner_router)

register_exception_handlers(app)

@app.get("/")
def root():
    return {"message": "RetailFish API"}


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "scheduler": scheduler.running,
    }

# source .venv/bin/activate
# pip freeze > requirements.txt
#  docker compose exec backend sh