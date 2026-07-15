# RetailFish

RetailFish is a production-ready, modular trading platform for discretionary and systematic traders.

It provides a unified workspace for market research, charting, stock screening, watchlists, technical analysis, and future portfolio, journaling, AI, and trading capabilities.

Built with a production-first mindset using modern architecture, Docker, and incremental sprint-based development.

---

## Features

### Market Data

- Historical candle data
- Live market quotes
- Multiple timeframe support
- Yahoo Finance provider
- Provider abstraction
- Historical data synchronization

### Charting

- TradingView Lightweight Charts
- Modular chart engine
- Volume overlay
- EMA indicators
- Responsive resizing
- Reset zoom
- Professional toolbar

### Scanner

- Modular scanner engine
- Strategy-based architecture
- Scanner scoring
- EMA Alignment
- Volume Breakout
- Relative Strength
- 52 Week High
- Trend Template
- Scanner sorting
- Scanner details
- Keyboard navigation

### Watchlists

- Multiple watchlists
- Add / Remove symbols
- Rename watchlists
- Live quotes
- Shared QuoteStore

### Performance

- Historical candle caching
- Scanner caching
- Quote caching
- Bulk quote loading
- Request deduplication

---

## Architecture

```text
                Browser
                    │
                    ▼
                 Nginx
          ┌─────────┴─────────┐
          ▼                   ▼
   Vue 3 Frontend      FastAPI Backend
                              │
             ┌────────────────┴──────────────┐
             ▼                               ▼
       Service Layer                 Provider Layer
             ▼                               ▼
      Repository Layer            Yahoo Finance
             ▼
        PostgreSQL
             ▼
           Redis
```

---

## Tech Stack

### Frontend

- Vue 3
- TypeScript
- Vite
- Pinia
- TradingView Lightweight Charts

### Backend

- FastAPI
- Python 3.12
- SQLAlchemy
- Alembic
- Pydantic

### Infrastructure

- PostgreSQL
- Redis
- Docker
- Docker Compose
- Nginx
- GitHub Actions

---

## Current Release

**Version:** `v0.4.0`

### Highlights

- Modular Chart Engine
- Indicator Engine
- Volume Overlay
- Professional Chart Toolbar
- Watchlists
- Shared Quote Engine
- Scanner Engine
- Scanner Sorting
- Performance Caching

---

## Getting Started

```bash
git clone <repository-url>
cd retailfish

cp .env.example .env

docker compose up --build
```

---

## Services

| Service     | URL                         |
| ----------- | --------------------------- |
| Frontend    | http://localhost            |
| Backend API | http://localhost/api        |
| Swagger     | http://localhost/api/docs   |
| Health      | http://localhost/api/health |

---

## Roadmap

| Version | Status  | Focus                        |
| ------- | ------- | ---------------------------- |
| v0.1    | ✅      | Platform Foundation          |
| v0.2    | ✅      | Market Data & Charts         |
| v0.3    | ✅      | Watchlists & Quote Engine    |
| v0.4    | ✅      | Technical Analysis & Scanner |
| v0.5    | 🚧      | Pattern Detection            |
| v0.6    | Planned | CANSLIM & Rankings           |
| v0.7    | Planned | Trading Engine               |
| v0.8    | Planned | Portfolio & Journal          |
| v0.9    | Planned | AI Research                  |
| v1.0    | Planned | Live Trading Platform        |

---

## Development Principles

- Production-first architecture
- Docker-first development
- SOLID & DRY principles
- Repository & Service patterns
- Provider abstraction
- Incremental sprint-based delivery
- Modular, extensible design

---

RetailFish is under active development. Every sprint delivers a fully deployable, production-quality feature while laying the foundation for a complete professional trading platform.
