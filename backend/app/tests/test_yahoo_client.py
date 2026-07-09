from app.clients.yahoo_finance_client import YahooFinanceClient

client = YahooFinanceClient()

candles = client.fetch_historical(
    symbol="RELIANCE.NS",
    timeframe="1d",
    limit=5,
)

print(type(candles))
print(len(candles))
print(candles[0])