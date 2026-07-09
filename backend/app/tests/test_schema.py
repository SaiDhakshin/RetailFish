from app.schemas.market_data import BackfillRequest

request = BackfillRequest(
    symbol="BTCUSDT",
    timeframe="1m",
    limit=100,
)

print(request)