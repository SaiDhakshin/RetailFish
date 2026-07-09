from app.clients.market_data_provider import MarketDataClient

client = MarketDataClient()

endpoint, params = client.build_historical_request(
    symbol="BTCUSDT",
    timeframe="1m",
    limit=5,
)

data = client.send_request(endpoint, params)

candles = client.normalize_history(data)

print(candles)

# Binance

# [
#   Open Time,
#   Open,
#   High,
#   Low,
#   Close,
#   Volume,
#   Close Time,
#   Quote Asset Volume,
#   Number Of Trades,
#   Taker Buy Base Volume,
#   Taker Buy Quote Volume,
#   Ignore
# ]