# Changelog

## [v0.4.0] - Technical Analysis & Scanner Foundation

### Added

#### Chart Architecture

- Modular ChartEngine
- CandleLayer abstraction
- VolumeLayer abstraction
- IndicatorManager
- Indicator framework
- Runtime indicator registration
- Dynamic indicator configuration
- Responsive chart resizing
- Chart reset zoom
- Chart fit content
- Volume visibility toggle

---

#### Indicators

- EMA 20
- EMA 50
- EMA 200
- Indicator store
- Indicator persistence
- Runtime indicator enable/disable
- Indicator configuration system

---

#### Scanner

- Modular scanner engine
- Scanner service
- Strategy-based scanner architecture
- Scanner result scoring
- Scanner details panel
- Scanner skeleton loader
- Scanner keyboard navigation
- Scanner sorting
- Scanner result selection
- Add scanner results to watchlists

---

#### Scanner Filters

- EMA Alignment
- Volume Breakout
- Relative Strength
- 52 Week High
- Trend Template

---

#### Scanner Sorting

- Score
- Relative Strength
- Volume Ratio
- Distance From 52 Week High
- Symbol
- Ascending / Descending sorting

---

#### Quotes

- Shared QuoteStore
- Quote cache
- Quote TTL
- Active symbol management
- Quote polling
- Manual refresh support
- Bulk quote loading
- Request deduplication
- Shared quote cache across application

---

#### Performance

- Scanner result caching
- Historical candle caching
- Indicator cache
- Bulk quote optimization
- Cached scanner execution
- Efficient frontend sorting

---

#### Dashboard

- Professional scanner sidebar
- Scanner details panel
- Chart toolbar
- Timeframe selector
- Indicator selector
- Refresh button
- Fit chart
- Reset zoom
- Live quote integration
- Responsive layout improvements

---

#### Backend

- Scanner service
- Scanner models
- Scanner schemas
- Indicator cache
- Scanner cache
- Bulk quote endpoint
- Quote service improvements
- Quote provider enhancements

---

#### APIs

- Scanner API
- Bulk Quote API improvements
- Extended scanner response model
- Quote polling support

---

## Changed

### Architecture

- Refactored chart into reusable modules
- Introduced ChartEngine abstraction
- Introduced IndicatorManager
- Introduced QuoteStore as single source of truth
- Improved scanner architecture
- Improved indicator architecture
- Improved component separation
- Improved state management
- Improved dependency boundaries

---

### Performance

- Reduced duplicate quote requests
- Optimized bulk quote loading
- Optimized scanner execution
- Improved frontend rendering
- Improved quote caching strategy
- Improved chart updates
- Improved scanner responsiveness

---

### UI

- Improved scanner workflow
- Improved watchlist integration
- Improved keyboard navigation
- Improved chart interactions
- Improved sidebar usability
- Improved sorting experience

---

## Fixed

- Quote flickering during polling
- Duplicate bulk quote requests
- Scanner selection persistence
- Chart resize issues
- Chart zoom reset behavior
- Quote cache edge cases
- Scanner loading synchronization
- Watchlist quote synchronization
- Scanner sorting stability
- Bulk quote response handling

---

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
- Watchlist Item API
- Quote API
- Bulk Quote API

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

---

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

---

## [v0.1.0] - Foundation

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
