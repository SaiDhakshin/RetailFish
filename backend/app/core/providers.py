from app.clients.binance_client import BinanceClient
from app.clients.market_data_provider import MarketDataProvider
from app.clients.yahoo_finance_client import YahooFinanceClient


def get_market_data_provider() -> MarketDataProvider:
    # return BinanceClient()
    """
    Return the configured market data provider.
    """
    return YahooFinanceClient()