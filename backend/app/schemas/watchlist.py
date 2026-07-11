from datetime import datetime

from pydantic import BaseModel, ConfigDict


class WatchlistCreate(BaseModel):
    """
    Request body for creating a watchlist.
    """

    name: str


class WatchlistUpdate(BaseModel):
    """
    Request body for renaming a watchlist.
    """

    name: str


class WatchlistResponse(BaseModel):
    """
    Watchlist response.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    name: str
    created_at: datetime
    updated_at: datetime


class WatchlistItemCreate(BaseModel):
    """
    Request body for adding a symbol.
    """

    symbol: str


class WatchlistItemResponse(BaseModel):
    """
    Watchlist item response.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    symbol: str
    created_at: datetime