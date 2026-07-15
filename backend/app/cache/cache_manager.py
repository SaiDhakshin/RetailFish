from datetime import datetime, timedelta
from typing import TypeVar

from app.cache.cache_entry import CacheEntry

T = TypeVar("T")


class CacheManager:
    """
    Simple in-memory cache with TTL support.
    """

    def __init__(self) -> None:
        self._cache: dict[str, CacheEntry] = {}

    def get(
        self,
        key: str,
    ) -> T | None:

        entry = self._cache.get(key)

        if entry is None:
            return None

        if datetime.utcnow() > entry.expires_at:
            del self._cache[key]
            return None

        return entry.value

    def set(
        self,
        key: str,
        value: T,
        ttl_seconds: int,
    ) -> None:

        self._cache[key] = CacheEntry(
            value=value,
            expires_at=datetime.utcnow()
            + timedelta(seconds=ttl_seconds),
        )

    def delete(
        self,
        key: str,
    ) -> None:

        self._cache.pop(key, None)

    def clear(self) -> None:
        self._cache.clear()