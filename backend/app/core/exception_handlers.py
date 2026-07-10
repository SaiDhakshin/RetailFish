from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.exceptions.instrument import (
    InstrumentNotFoundError,
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