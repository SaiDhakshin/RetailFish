from pprint import pprint

from app.clients.binance_client import BinanceClient

client = BinanceClient()

candles = client.fetch_historical(
    symbol="BTCUSDT",
    timeframe="1m",
    limit=5,
)

print(len(candles))
print()

pprint(candles[0])

print(type(candles))
print(type(candles[0]))