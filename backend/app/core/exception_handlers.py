from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import Request

from app.exceptions.instrument import (
    InstrumentNotFoundError,
)

from app.exceptions.watchlist import (
    InstrumentAlreadyInWatchlistError,
)


def register_exception_handlers(
    app: FastAPI,
):

    @app.exception_handler(
        InstrumentNotFoundError
    )
    async def instrument_not_found(
        request,
        exc,
    ):

        return JSONResponse(
            status_code=404,
            content={
                "detail": str(exc),
            },
        )
    
    @app.exception_handler(
        InstrumentAlreadyInWatchlistError,
    )
    async def duplicate_watchlist_item(
        request: Request,
        exc: InstrumentAlreadyInWatchlistError,
    ):

        return JSONResponse(
            status_code=409,
            content={
                "detail": str(exc),
            },
        )