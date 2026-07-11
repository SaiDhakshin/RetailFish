from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.watchlist import (
    WatchlistCreate,
    WatchlistItemCreate,
    WatchlistItemResponse,
    WatchlistResponse,
    WatchlistUpdate,
)
from app.services.watchlist_service import WatchlistService

router = APIRouter(
    prefix="/watchlists",
    tags=["Watchlists"],
)

@router.get(
    "",
    response_model=list[WatchlistResponse],
)
def get_watchlists(
    db: Session = Depends(get_db),
):

    service = WatchlistService(db)

    return service.list_watchlists()


@router.post(
    "",
    response_model=WatchlistResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_watchlist(
    request: WatchlistCreate,
    db: Session = Depends(get_db),
):

    service = WatchlistService(db)

    try:

        return service.create_watchlist(
            request.name,
        )

    except Exception as exc:
        raise
    
@router.patch(
    "/{watchlist_id}",
    response_model=WatchlistResponse,
)
def rename_watchlist(
    watchlist_id: int,
    request: WatchlistUpdate,
    db: Session = Depends(get_db),
):

    service = WatchlistService(db)

    try:

        return service.rename_watchlist(
            watchlist_id,
            request.name,
        )

    except Exception as exc:
        raise 
    
@router.delete(
"/{watchlist_id}",
status_code=status.HTTP_204_NO_CONTENT,
)
def delete_watchlist(
    watchlist_id: int,
    db: Session = Depends(get_db),
):

    service = WatchlistService(db)

    service.delete_watchlist(
        watchlist_id,
    )

@router.get(
    "/{watchlist_id}/items",
    response_model=list[WatchlistItemResponse],
)
def get_items(
    watchlist_id: int,
    db: Session = Depends(get_db),
):

    service = WatchlistService(db)

    return service.list_items(
        watchlist_id,
    )

@router.post(
    "/{watchlist_id}/items",
    response_model=WatchlistItemResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_symbol(
    watchlist_id: int,
    request: WatchlistItemCreate,
    db: Session = Depends(get_db),
):

    service = WatchlistService(db)

    try:

        return service.add_symbol(
            watchlist_id,
            request.symbol,
        )

    except Exception as exc:
        raise
    
@router.delete(
    "/{watchlist_id}/items/{instrument_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_symbol(
    watchlist_id: int,
    instrument_id: int,
    db: Session = Depends(get_db),
):

    service = WatchlistService(db)

    service.remove_symbol(
        watchlist_id,
        instrument_id,
    )