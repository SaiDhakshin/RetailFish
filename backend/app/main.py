from fastapi import FastAPI

from app.api.market_data import router as market_router

from app.api.instruments import (
    router as instrument_router,
)

from app.api.candles import (
    router as candle_router,
)

from app.api.history import router as history_router

from app.core.exception_handlers import (
    register_exception_handlers,
)


app = FastAPI(
    title="Trading OS Backend",
    version="0.1.0"
)

app.include_router(market_router)

app.include_router(instrument_router)

app.include_router(candle_router)

app.include_router(history_router)

register_exception_handlers(app)

@app.get("/")
def root():
    return {"message": "RetailFish API"}


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

# source .venv/bin/activate
# pip freeze > requirements.txt
#  docker compose exec backend sh