from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):

    APP_NAME: str = "RetailFish"

    DEFAULT_TIMEFRAME: str = "1d"

    DEFAULT_LIMIT: int = 1000

    YAHOO_TIMEOUT: int = 30

    HISTORY_SYNC_ENABLED: bool = True

    HISTORY_SYNC_HOUR: int = 18

    HISTORY_SYNC_MINUTE: int = 0

    HISTORY_SYNC_TIMEFRAMES: str = "1d"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()