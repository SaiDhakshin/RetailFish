from app.clients.nse_symbol_provider import NSESymbolProvider

provider = NSESymbolProvider()

symbols = provider.fetch_symbols()

print("Total:", len(symbols))

print(symbols[:20])

# docker compose exec backend python -m app.tests.test_nse_symbol_provider