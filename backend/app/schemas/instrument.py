from pydantic import BaseModel, ConfigDict


class InstrumentResponse(BaseModel):
    """
    Response model for an instrument.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    symbol: str
    name: str | None = None
    exchange: str | None = None
    sector: str | None = None
    industry: str | None = None


class InstrumentSearchResponse(BaseModel):
    """
    Response returned by the search endpoint.
    """

    total: int
    items: list[InstrumentResponse]