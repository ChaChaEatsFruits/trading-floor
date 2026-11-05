# Trading Floor

Four AI traders - Warren (value), George (macro), Ray (systematic) and Cathie (crypto) - each
manage a simulated account through MCP servers. Every trader is an agent on the OpenAI Agents SDK
that calls three servers directly (accounts, market data, push notifications) and delegates
research to a researcher sub-agent that has Fetch, Tavily web search and a per-trader Memory
(libSQL) server. A FastAPI backend serves the data to a Vite + TypeScript frontend that shows the floor live.

## How it works

- `backend/traders.py` - the `Trader` agent and its researcher tool; picks the model client
- `backend/trading_floor.py` - the four traders, their models, and the run loop
- `backend/accounts*.py`, `database.py` - account state in SQLite, served over MCP
- `backend/market*.py` - Massive market data when a key is set, otherwise simulated prices
- `backend/mcp_servers.py` - the MCP servers for the traders and the researcher
- `backend/tracers.py` - `LogTracer`, which writes every SDK trace span to the database for the live log
- `backend/api.py` - read-only FastAPI endpoints: traders, portfolio value, holdings, transactions, logs, market source
- `frontend/` - Vite + TypeScript app (uPlot): per-trader portfolio chart, holdings heatmap, activity log,
  transactions, dark/light theme, and a simulated/live market badge. In dev, Vite proxies `/api` to port 8000.

## Models

All four traders default to `gpt-6-sol`. Set `USE_MANY_MODELS=true` to give each a different
provider's model (GPT, DeepSeek, Gemini, Grok); that needs the matching keys in `.env`.

## Setup

Requires Python 3.12+, [uv](https://docs.astral.sh/uv/) and Node.js (`npx`).

```
cp .env.example .env                        # add OPENAI_API_KEY, plus TAVILY_API_KEY for web search
uv sync
cd frontend && npm install && cd ..
```

Run three terminals:

```
uv run uvicorn backend.api:app --port 8000  # API (docs at http://localhost:8000/docs)
cd frontend && npm run dev                  # UI at http://localhost:5173
uv run -m backend.trading_floor             # the trading engine
```

Optional: `MASSIVE_API_KEY` for real prices, `PUSHOVER_USER`/`PUSHOVER_TOKEN` for notifications.
`RUN_EVERY_N_MINUTES` (default 60) sets the cadence, and the floor skips runs while the market is
closed unless `RUN_EVEN_WHEN_MARKET_IS_CLOSED=true`. The engine loops until stopped, so watch your API usage.
