# Sprint 4 — Technical Analysis

**Version:** v0.4.0

---

# Goal

Transform RetailFish from a market viewer into a professional charting and technical analysis platform.

---

# Phase 1 — Chart Architecture

## Issue 1 — Chart Refactor

### Objective

Split TradingChart into reusable modules before introducing indicators.

### Tasks

#### Chart Core

- [ ] Create ChartManager
- [ ] Move chart creation logic
- [ ] Move resize handling
- [ ] Move chart cleanup
- [ ] Move chart options

---

#### Candle Management

- [ ] Create CandleSeries
- [ ] Create candlestick series
- [ ] Update candles
- [ ] Replace candles
- [ ] Clear candles

---

#### Crosshair

- [ ] Create CrosshairManager
- [ ] Crosshair synchronization
- [ ] Tooltip support

---

#### Time Scale

- [ ] Create TimeScaleManager
- [ ] Fit content
- [ ] Reset zoom
- [ ] Visible range helpers

---

### Deliverable

```
TradingChart.vue

↓

ChartManager

↓

CandleSeries

↓

CrosshairManager

↓

TimeScaleManager
```

---

# Phase 2 — Indicator Engine

## Issue 2 — Indicator Framework

### Tasks

#### Indicator Types

- [ ] Indicator interface
- [ ] Indicator options
- [ ] Indicator visibility
- [ ] Indicator colors

---

#### Indicator Store

- [ ] Pinia store
- [ ] Enable/Disable indicators
- [ ] Persist settings
- [ ] Indicator configuration

---

#### Indicator Services

- [ ] Base indicator utilities
- [ ] EMA
- [ ] SMA
- [ ] RSI
- [ ] MACD
- [ ] VWAP
- [ ] ATR
- [ ] Bollinger Bands

---

#### Indicator Manager

- [ ] Create IndicatorManager
- [ ] Register indicators
- [ ] Create line series
- [ ] Update series
- [ ] Remove series

---

### Deliverable

Reusable indicator engine.

---

# Phase 3 — Volume

## Issue 3 — Volume Overlay

### Tasks

- [ ] Volume calculation
- [ ] Histogram series
- [ ] Green/Red colors
- [ ] Toggle visibility

### Deliverable

Volume bars under candles.

---

# Phase 4 — EMA

## Issue 4 — EMA

### Tasks

- [ ] EMA 20
- [ ] EMA 50
- [ ] EMA 200
- [ ] Overlay chart
- [ ] Toggle visibility
- [ ] Custom colors

### Deliverable

EMA overlays.

---

# Phase 5 — RSI

## Issue 5 — RSI

### Tasks

- [ ] RSI calculation
- [ ] Separate panel
- [ ] 30/70 guide lines
- [ ] Toggle visibility

### Deliverable

RSI indicator.

---

# Phase 6 — MACD

## Issue 6 — MACD

### Tasks

- [ ] MACD line
- [ ] Signal line
- [ ] Histogram
- [ ] Toggle visibility

### Deliverable

MACD panel.

---

# Phase 7 — Advanced Indicators

## Issue 7

### VWAP

- [ ] VWAP calculation
- [ ] Overlay

### ATR

- [ ] ATR calculation

### Bollinger Bands

- [ ] Upper band
- [ ] Middle band
- [ ] Lower band
- [ ] Band fill

### Deliverable

Advanced indicator suite.

---

# Phase 8 — Toolbar

## Issue 8 — Chart Toolbar

### Tasks

- [ ] Timeframe selector
- [ ] Indicator selector
- [ ] Refresh
- [ ] Fit chart
- [ ] Reset zoom
- [ ] Indicator settings

### Deliverable

Professional toolbar.

---

# Sprint Deliverables

## Chart

- [ ] Modular architecture
- [ ] Candle manager
- [ ] Crosshair manager
- [ ] Time scale manager

---

## Indicators

- [ ] EMA
- [ ] SMA
- [ ] RSI
- [ ] MACD
- [ ] VWAP
- [ ] ATR
- [ ] Bollinger Bands

---

## UI

- [ ] Toolbar
- [ ] Indicator settings
- [ ] Volume panel

---

# Version

**v0.4.0 — Technical Analysis**
