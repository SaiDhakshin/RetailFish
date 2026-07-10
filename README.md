# RetailFish

A production-ready, modular trading platform built for discretionary and systematic trading.

The goal of RetailFish is to provide a single platform for market research, stock screening, pattern detection, trade journaling, paper trading, live execution, portfolio management, AI-assisted analysis, and quantitative research.

The project is being developed incrementally using sprint-based releases. Every release is fully deployable and usable.

---

# Vision

RetailFish is designed around these principles:

- Production-first architecture
- Docker-first development
- SOLID and DRY design principles
- Modular plugin-based architecture
- Event-driven design
- AI as an assistant, not a decision maker
- Incremental delivery
- Multi-asset support
- Multi-broker support
- Complete audit trail

---

# Long-Term Goals

## Supported Asset Classes

- Indian Equities
- ETFs
- Futures
- Options
- Crypto
- Crypto Perpetual Futures

---

## Planned Features

### Market Data

- Historical data
- Real-time streaming
- Multiple data providers
- Corporate actions
- Fundamentals
- News
- Economic calendar

### Screening

- Custom screeners
- Saved screeners
- Sector ranking
- Industry ranking
- Relative Strength
- CANSLIM scoring

### Pattern Detection

- Cup & Handle
- Volatility Contraction Pattern (VCP)
- Double Bottom
- Flat Base
- IPO Base
- High Tight Flag
- Ascending Base

### Trading

- Swing Trading
- Intraday Trading
- Paper Trading
- Live Trading

### Journal

- Trade journal
- Chart snapshots
- Trade reviews
- Statistics
- Performance analytics

### Portfolio

- Holdings
- Positions
- Risk
- Exposure
- Analytics

### AI

- Market summaries
- Pattern explanations
- Trade review
- Journal coaching
- Research assistant

### Research

- Backtesting
- Strategy comparison
- Historical analysis
- Replay engine
- Performance statistics

---

# Current Release

**Version:** v0.2.0

## Completed

### Foundation

- Docker Compose
- FastAPI backend
- Vue 3 frontend
- PostgreSQL
- Redis
- Nginx
- Environment configuration
- Health check endpoint
- GitHub Actions CI

### Market Data

- NSE instrument import
- Yahoo Finance provider
- Binance provider abstraction
- Historical candle import
- Automatic history caching
- Duplicate prevention
- DTO-based provider architecture
- Mapper layer
- Repository pattern
- Service layer

### APIs

- Instrument Search API
- Historical Candle API
- Manual History Import API

### Frontend

- Stock search
- Debounced search
- Keyboard navigation
- TradingView Lightweight Charts
- Automatic candle loading

# Tech Stack

## Frontend

- Vue 3
- TypeScript
- Vite
- Pinia
- Tailwind CSS

## Backend

- FastAPI
- Python 3.12
- SQLAlchemy
- Alembic
- Pydantic
- yfinance

## Database

- PostgreSQL

## Cache

- Redis

## Reverse Proxy

- Nginx

## Infrastructure

- Docker
- Docker Compose
- GitHub Actions

---

# Project Structure

```text
trading-os/

├── backend/
├── frontend/
├── docker/
├── nginx/
├── docs/
├── scripts/
├── .github/
├── docker-compose.yml
├── .env.example
└── README.md
```

---

# Architecture

```text
                    Browser
                        │
                        ▼
                     Nginx
               ┌────────┴────────┐
               ▼                 ▼
         Vue Frontend      FastAPI Backend
                                  │
                 ┌────────────────┴────────────────┐
                 ▼                                 ▼
          Service Layer                     Provider Layer
                 │                                 │
                 ▼                                 ▼
         Repository Layer                  Yahoo / Binance
                 │                                 │
                 └────────────────┬────────────────┘
                                  ▼
                             PostgreSQL
                                  │
                                  ▼
                                Redis
```

# Development Principles

- Build vertically (complete features end-to-end).
- Every sprint produces a usable feature.
- Every release is deployable.
- Refactor only when it provides clear value.
- Add abstractions when multiple implementations exist.
- Keep business logic deterministic.
- Use AI only for explanation, research, and productivity.

---

# Development Workflow

Every feature follows the same lifecycle:

```text
Issue
    │
    ▼
Create Branch
    │
    ▼
Develop
    │
    ▼
Test
    │
    ▼
Docker
    │
    ▼
Merge
    │
    ▼
Deploy
```

---

# Design Patterns

RetailFish currently uses:

- Repository Pattern
- Service Layer
- Provider Pattern
- DTO Pattern
- Mapper Pattern
- Dependency Injection
- Factory Pattern

# Backend Architecture

The backend follows a layered architecture.

```text
API

↓

Service

↓

Repository

↓

Database
```

Market data follows a provider-based architecture.

```text
Provider

↓

DTO

↓

Mapper

↓

Repository

↓

Database
```

This separation keeps business logic independent of external providers and allows new providers to be added with minimal changes.

# Getting Started

## Clone the repository

```bash
git clone <repository-url>
cd trading-os
```

## Configure environment

```bash
cp .env.example .env
```

Update the values in `.env` as required.

## Start the application

```bash
docker compose up --build
```

---

# Services

| Service      | URL                         |
| ------------ | --------------------------- |
| Frontend     | http://localhost            |
| Backend API  | http://localhost/api        |
| Swagger UI   | http://localhost/api/docs   |
| Health Check | http://localhost/api/health |

---

# Core API Endpoints

## Instruments

```http
GET /api/instruments?q=reli
```

## Candles

```http
GET /api/candles?symbol=RELIANCE.NS&timeframe=1d
```

## Historical Import

```http
POST /api/history/import
```

# Roadmap

## v0.1

- Foundation
- Docker
- Backend
- Frontend
- Database
- Redis

## v0.2 ✅

- NSE Instrument Import
- Historical Candle Import
- Yahoo Finance Provider
- Provider Abstraction
- TradingView Charts
- Instrument Search
- Historical Candle API

## v0.3

- Watchlists
- Multiple Timeframes
- Technical Indicators
- Daily Synchronization
- Redis Caching

## v0.4

- Indicator Engine

## v0.5

- Screener

## v0.6

- Pattern Detection

## v0.7

- CANSLIM

## v0.8

- Sector Ranking

## v0.9

- Trade Journal

## v1.0

- Paper Trading

---

# Sprint Philosophy

This project is developed using short, incremental sprints.

Each sprint must satisfy one rule:

> Every sprint ends with a feature that can be used.

Features are completed one at a time and deployed before moving to the next sprint.

---

# Sprint Progress

| Sprint   | Status      | Description             |
| -------- | ----------- | ----------------------- |
| Sprint 1 | ✅ Complete | Platform Foundation     |
| Sprint 2 | ✅ Complete | Market Data & Charts    |
| Sprint 3 | 🚧 Planned  | Watchlists & Indicators |
| Sprint 4 | Planned     | Screener                |
| Sprint 5 | Planned     | Pattern Detection       |
| Sprint 6 | Planned     | Trading Engine          |
| Sprint 7 | Planned     | Portfolio               |
| Sprint 8 | Planned     | AI Research             |

# License

This project is currently under active development.

A project license will be added before public release.
