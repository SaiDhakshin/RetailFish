from app.clients.binance_client import BinanceClient

client = BinanceClient()

print(client.client.base_url)
print(client.client.timeout)

print(client.get_exchange_timeframe("1m"))
print(client.get_exchange_timeframe("5m"))
print(client.get_exchange_timeframe("1h"))
print(client.get_exchange_timeframe("1d"))

endpoint, params = client.build_historical_request(
    symbol="BTCUSDT",
    timeframe="1m",
    limit=10,
)

print(endpoint)
print(params)