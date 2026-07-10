from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):

    APP_NAME: str = "RetailFish"

    DEFAULT_TIMEFRAME: str = "1d"

    DEFAULT_LIMIT: int = 500

    YAHOO_TIMEOUT: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()