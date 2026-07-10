# Sprint 02 — Market Data & Chart Foundation

## Sprint Goal

Build the market data foundation for RetailFish.

By the end of this sprint, I should be able to:

1. Search for an NSE stock.
2. Select the stock.
3. Retrieve historical market data.
4. Display a candlestick chart.

This is the first user-facing trading feature.

---

# Sprint Duration

- Start: 2026-07-08
- End: 2026-07-10

---

# Definition of Done

Sprint 2 is complete when:

- [x] I can search for a stock.
- [x] Search results are loaded from the database.
- [x] Historical OHLCV data is stored in PostgreSQL.
- [x] Backend API returns historical candles.
- [x] Frontend displays a candlestick chart.
- [x] Everything works through Docker Compose.
- [x] GitHub Actions pass successfully.
- [x] Documentation is updated.

---

# Sprint Goal Flow

```text
Open Trading OS

↓

Search "RELIANCE"

↓

Select Stock

↓

Backend Fetches Data

↓

Historical Candles Loaded

↓

Candlestick Chart Displayed
```

---

# Epic

**Market Data**

---

# Sprint Backlog

## Issue 1 — Instrument Master

### Goal

Create and maintain a master list of tradable instruments.

### Tasks

- [x] Design Instrument database table
- [x] Download NSE instrument list
- [x] Store instruments in PostgreSQL
- [x] Create import script
- [x] Add indexes
- [x] Validate imported data

### Done When

- [x] Instrument search works
- [x] Instruments are stored in PostgreSQL

---

## Issue 2 — Historical Market Data

### Goal

Download and store historical OHLCV data.

### Tasks

- [x] Select market data provider
- [x] Download historical candles
- [x] Store OHLCV data
- [x] Prevent duplicate records
- [x] Handle missing data
- [x] Add retry logic

### Done When

- [x] Historical data exists for selected symbols

---

## Issue 3 — Database

### Goal

Create the market data schema.

### Tables

- [x] Instrument
- [x] OHLCV

### Done When

- [x] Alembic migrations completed
- [x] Database migrations succeed

---

## Issue 4 — Market Data Service

### Goal

Create the service responsible for downloading and retrieving market data.

### Responsibilities

- Download data
- Store data
- Retrieve data
- Update data

### Done When

- [x] Service can retrieve historical candles

---

## Issue 5 — Search API

### Endpoint

```http
GET /api/instruments?q=
```

### Tasks

- [x] Search by symbol
- [x] Search by company name
- [x] Return matching instruments

### Done When

- [x] API returns matching stocks

---

## Issue 6 — Candle API

### Endpoint

```http
GET /api/candles
```

### Query Parameters

- symbol
- timeframe

### Done When

- [x] API returns OHLCV data

---

## Issue 7 — Search UI

### Goal

Allow users to search for instruments.

### Tasks

- [x] Search input
- [x] Debounced search
- [x] Search results
- [x] Select instrument

### Done When

- [x] User can select a stock

---

## Issue 8 — Candlestick Chart

### Goal

Display historical candles.

### Tasks

- [x] Integrate TradingView Lightweight Charts
- [x] Render OHLCV candles
- [x] Support resize
- [x] Support zoom
- [x] Support pan

### Done When

- [x] Candlestick chart displays correctly

---

# Architecture

## Backend

```
backend/

market_data/

instrument/

api/

database/
```

---

## Frontend

```
frontend/

components/

pages/

services/

types/
```

---

# Database

## Instrument

- id
- symbol
- name
- exchange
- isin
- active

---

## OHLCV

- instrument_id
- timestamp
- open
- high
- low
- close
- volume

---

# Out of Scope

The following features are intentionally excluded from this sprint:

- Indicators
- EMA
- RSI
- ATR
- ADX
- Pattern Detection
- CANSLIM
- Sector Ranking
- AI
- Trade Journal
- Portfolio
- Paper Trading
- Broker Integration
- Crypto
- Options

---

# Deliverable

At the end of Sprint 2:

```text
Trading OS

↓

Search Stock

↓

Select Stock

↓

Historical Data

↓

Candlestick Chart
```

---

# Success Criteria

The sprint is successful if:

- The application runs through Docker Compose.
- Search works correctly.
- Historical market data is available.
- The candlestick chart renders successfully.
- The feature is production-ready.
- The release can be tagged as **v0.2.0**.

---

# Sprint Retrospective

## What went well?

Fetching and storing OHLCV and rendering went well.

## What slowed me down?

When chaning code to from fixed binance to support yahoo felt like giving up.

## Lessons Learned

Push through

## Improvements for Sprint 3

Watchlists.
