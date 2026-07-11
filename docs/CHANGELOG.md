# Changelog

## v0.1.0 - Foundation

### Added

- Docker Compose
- Vue frontend
- FastAPI backend
- PostgreSQL
- Redis
- Nginx
- GitHub Actions
- Health endpoint
- CI validation

# [v0.2.0] - Sprint 2

## Added

### Charts

- Interactive candlestick chart
- Lightweight Charts integration
- Responsive chart resizing
- OHLCV visualization

### Market Data

- Historical candle API
- Candle repository
- Market data service
- Yahoo Finance historical downloader

### Instruments

- Instrument database
- Instrument API
- Instrument search
- Instrument repository

### Dashboard

- Trading dashboard
- Search component
- Timeframe selector
- Chart integration

### Backend

- Historical data service
- Instrument service
- Market data provider abstraction
- Yahoo Finance provider

### APIs

- Candle API
- Instrument API
- Historical synchronization API

---

## Changed

- Refactored backend service architecture
- Improved repository abstraction
- Improved market data loading
- Standardized API responses

---

## Fixed

- Historical candle synchronization
- Timezone normalization
- Yahoo Finance download issues
- Database persistence issues

# [v0.3.0] - Sprint 3

## Added

### Historical Data

- Historical synchronization service
- Incremental candle synchronization
- Background historical scheduler
- Configurable scheduler settings
- Scheduler progress logging
- Automatic daily market synchronization

### Watchlists

- Watchlist management
- Multiple watchlists
- Watchlist items
- Add symbol to watchlist
- Remove symbol from watchlist
- Rename watchlists
- Delete watchlists
- Duplicate symbol validation

### Quotes

- Live market quote service
- Quote provider abstraction
- Yahoo Finance quote provider
- Bulk quote API
- Automatic quote refresh
- Quote caching

### Dashboard

- Watchlist sidebar
- Active watchlist highlighting
- Active symbol highlighting
- Resizable sidebar
- Add-to-watchlist dialog

### Search

- Instrument search
- Debounced search
- Keyboard navigation
- Live quotes inside search
- Bulk quote integration

### Backend

- Quote service
- Watchlist service
- Watchlist repositories
- Historical synchronization service
- APScheduler integration
- Scheduler configuration

### APIs

- Watchlist CRUD API
- Watchlist item API
- Quote API
- Bulk quote API

---

## Changed

- Improved dashboard layout
- Improved quote loading performance
- Refactored market data provider abstraction
- Improved scheduler logging
- Improved watchlist state management
- Optimized quote loading using bulk requests

---

## Fixed

- Duplicate watchlist entries
- Historical synchronization issues
- Scheduler startup issues
- Yahoo Finance timezone handling
- Quote loading edge cases
