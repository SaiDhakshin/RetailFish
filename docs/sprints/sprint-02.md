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
- End: _(To be updated)_

---

# Definition of Done

Sprint 2 is complete when:

- [ ] I can search for a stock.
- [ ] Search results are loaded from the database.
- [ ] Historical OHLCV data is stored in PostgreSQL.
- [ ] Backend API returns historical candles.
- [ ] Frontend displays a candlestick chart.
- [ ] Everything works through Docker Compose.
- [ ] GitHub Actions pass successfully.
- [ ] Documentation is updated.

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

- [ ] Design Instrument database table
- [ ] Download NSE instrument list
- [ ] Store instruments in PostgreSQL
- [ ] Create import script
- [ ] Add indexes
- [ ] Validate imported data

### Done When

- [ ] Instrument search works
- [ ] Instruments are stored in PostgreSQL

---

## Issue 2 — Historical Market Data

### Goal

Download and store historical OHLCV data.

### Tasks

- [ ] Select market data provider
- [ ] Download historical candles
- [ ] Store OHLCV data
- [ ] Prevent duplicate records
- [ ] Handle missing data
- [ ] Add retry logic

### Done When

- [ ] Historical data exists for selected symbols

---

## Issue 3 — Database

### Goal

Create the market data schema.

### Tables

- [ ] Instrument
- [ ] OHLCV

### Done When

- [ ] Alembic migrations completed
- [ ] Database migrations succeed

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

- [ ] Service can retrieve historical candles

---

## Issue 5 — Search API

### Endpoint

```http
GET /api/instruments?q=
```

### Tasks

- [ ] Search by symbol
- [ ] Search by company name
- [ ] Return matching instruments

### Done When

- [ ] API returns matching stocks

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

- [ ] API returns OHLCV data

---

## Issue 7 — Search UI

### Goal

Allow users to search for instruments.

### Tasks

- [ ] Search input
- [ ] Debounced search
- [ ] Search results
- [ ] Select instrument

### Done When

- [ ] User can select a stock

---

## Issue 8 — Candlestick Chart

### Goal

Display historical candles.

### Tasks

- [ ] Integrate TradingView Lightweight Charts
- [ ] Render OHLCV candles
- [ ] Support resize
- [ ] Support zoom
- [ ] Support pan

### Done When

- [ ] Candlestick chart displays correctly

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

_To be completed at the end of the sprint._

## What slowed me down?

_To be completed at the end of the sprint._

## Lessons Learned

_To be completed at the end of the sprint._

## Improvements for Sprint 3

_To be completed at the end of the sprint._
