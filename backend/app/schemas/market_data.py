from pydantic import BaseModel, Field


class BackfillRequest(BaseModel):
    symbol: str = Field(
        ...,
        description="Trading symbol",
        examples=["BTCUSDT"],
    )

    timeframe: str = Field(
        ...,
        description="Candle timeframe",
        examples=["1m"],
    )

    limit: int = Field(
        default=500,
        ge=1,
        le=1000,
        description="Number of candles to fetch",
    )


class BackfillResponse(BaseModel):
    symbol: str

    timeframe: str

    requested: int

    inserted: int

    skipped: int