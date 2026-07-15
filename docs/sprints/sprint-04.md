# Sprint 4 — Technical Analysis

**Version:** v0.4.0

---

# Goal

Transform RetailFish from a market viewer into a professional technical analysis and stock screening platform.

---

# Phase 1 — Chart Architecture

## Issue 1 — Chart Refactor

### Objective

Refactor the chart into reusable modules before introducing advanced indicators.

### Completed

#### Chart Core

- [x] ChartEngine
- [x] Chart creation abstraction
- [x] Resize handling
- [x] Chart cleanup
- [x] Chart configuration
- [x] Responsive resizing

---

#### Candle Management

- [x] CandleLayer
- [x] Candlestick series
- [x] Replace candles
- [x] Update candles
- [x] Clear candles
- [x] Auto fit content
- [x] Reset zoom support

---

#### Time Scale

- [x] Fit content
- [x] Reset zoom
- [ ] Visible range helpers

---

#### Crosshair

- [ ] CrosshairManager
- [ ] Tooltip support
- [ ] Crosshair synchronization

---

### Deliverable

```
TradingChart

↓

ChartEngine

├── CandleLayer
├── VolumeLayer
├── IndicatorManager
└── Resize Handling
```

---

# Phase 2 — Indicator Engine

## Issue 2 — Indicator Framework

### Completed

#### Indicator Framework

- [x] Indicator interface
- [x] Indicator configuration
- [x] Indicator visibility
- [x] IndicatorManager
- [x] Dynamic indicator registration
- [x] Runtime indicator updates

---

#### Indicator Store

- [x] Pinia store
- [x] Enable / Disable indicators
- [x] Persist configuration
- [x] Runtime updates

---

#### Implemented Indicators

- [x] EMA 20
- [x] EMA 50
- [x] EMA 200

---

#### Planned

- [ ] SMA
- [ ] RSI
- [ ] MACD
- [ ] VWAP
- [ ] ATR
- [ ] Bollinger Bands

---

### Deliverable

Reusable indicator engine.

---

# Phase 3 — Volume

## Issue 3 — Volume Overlay

### Completed

- [x] Histogram series
- [x] Green / Red colors
- [x] Toggle visibility
- [x] Volume panel

---

### Deliverable

Professional volume overlay.

---

# Phase 4 — Scanner Foundation

## Issue 4 — Scanner

### Completed

### Backend

- [x] Modular scanner engine
- [x] ScannerService
- [x] Strategy architecture
- [x] ScanResult model
- [x] Indicator cache
- [x] Scanner API

---

### Scanner Filters

- [x] EMA Alignment
- [x] Volume Breakout
- [x] Relative Strength
- [x] 52 Week High
- [x] Trend Template

---

### Scanner UI

- [x] Scanner sidebar
- [x] Scanner controls
- [x] Scanner details
- [x] Scanner skeleton
- [x] Keyboard navigation
- [x] Add to watchlist

---

### Sorting

- [x] Score
- [x] Relative Strength
- [x] Volume Ratio
- [x] Distance From High
- [x] Symbol
- [x] Ascending / Descending

---

### Deliverable

Production-ready scanner foundation.

---

# Phase 5 — Quote Engine

## Issue 5 — Quote Management

### Completed

- [x] Shared QuoteStore
- [x] Bulk Quote API
- [x] Quote caching
- [x] TTL support
- [x] Pending request deduplication
- [x] Shared quote cache
- [x] Active symbol management
- [x] Polling architecture
- [x] Manual refresh support
- [x] Ready for realtime providers

---

### Deliverable

Centralized quote management.

---

# Phase 6 — Toolbar

## Issue 6 — Chart Toolbar

### Completed

- [x] Timeframe selector
- [x] Indicator selector
- [x] Refresh
- [x] Fit chart
- [x] Reset zoom

---

### Remaining

- [ ] Indicator settings panel

---

### Deliverable

Professional chart toolbar.

---

# Phase 7 — Performance

## Issue 7 — Performance Improvements

### Completed

Backend

- [x] Historical candle cache
- [x] Scanner cache
- [x] Indicator cache
- [x] Bulk quote endpoint

Frontend

- [x] Shared quote cache
- [x] Bulk quote loading
- [x] Cached scanner results
- [x] Efficient sorting
- [x] Skeleton loading

---

### Deliverable

Production-ready performance optimizations.

---

# Sprint Deliverables

## Chart

- [x] Modular architecture
- [x] ChartEngine
- [x] CandleLayer
- [x] VolumeLayer
- [x] IndicatorManager

---

## Indicators

- [x] EMA
- [ ] SMA
- [ ] RSI
- [ ] MACD
- [ ] VWAP
- [ ] ATR
- [ ] Bollinger Bands

---

## Scanner

- [x] Scanner engine
- [x] Scanner UI
- [x] Sorting
- [x] Keyboard navigation
- [x] Scanner details
- [x] Watchlist integration

---

## Quotes

- [x] Shared QuoteStore
- [x] Bulk quote API
- [x] Quote caching
- [x] Polling support
- [x] Manual refresh

---

## UI

- [x] Toolbar
- [x] Volume panel
- [x] Responsive chart
- [x] Skeleton loading

---

# Version

**v0.4.0 — Technical Analysis & Scanner Foundation**
