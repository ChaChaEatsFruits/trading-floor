# Trading Floor

Four AI traders - Warren (value), George (macro), Ray (systematic) and Cathie (crypto) - each
manage a simulated account through MCP servers. Every trader is an agent on the OpenAI Agents SDK
that calls three servers directly (accounts, market data, push notifications) and delegates
research to a researcher sub-agent that has Fetch, Tavily web search and a per-trader Memory
(libSQL) server. A Gradio dashboard shows the floor live.

## How it works

- `backend/traders.py` - the `Trader` agent and its researcher tool; picks the model client
- `backend/trading_floor.py` - the four traders, their models, and the run loop
- `backend/accounts*.py`, `database.py` - account state in SQLite, served over MCP
- `backend/market*.py` - Massive market data when a key is set, otherwise simulated prices
- `backend/mcp_servers.py` - the MCP servers for the traders and the researcher
- `backend/api.py` - FastAPI endpoints used by the dashboard
- `demo/` - Gradio dashboard; `frontend/` - optional Vite + uPlot charts

## Models

All four traders default to `gpt-6-sol`. Set `USE_MANY_MODELS=true` to give each a different
provider's model (GPT, DeepSeek, Gemini, Grok); that needs the matching keys in `.env`.

## Setup

Requires Python 3.12+, [uv](https://docs.astral.sh/uv/) and Node.js (`npx`).

```
cp .env.example .env   # add OPENAI_API_KEY, plus TAVILY_API_KEY for web search
uv run app.py          # dashboard
```

Optional: `MASSIVE_API_KEY` for real prices, `PUSHOVER_USER`/`PUSHOVER_TOKEN` for notifications.
`RUN_EVERY_N_MINUTES` (default 60) sets the cadence, and the floor skips runs while the market is
closed unless `RUN_EVEN_WHEN_MARKET_IS_CLOSED=true`.

Frontend (optional): `cd frontend && npm install && npm run dev`.

## Verified

One full cycle for one trader (Warren) ran on `gpt-6-sol`: it read its account, changed its
strategy and bought VTI and VXUS through the accounts server, and the API listed all four
traders as "GPT 6 Sol". Not exercised: the Gradio dashboard, the Vite frontend, the other three
traders, `USE_MANY_MODELS=true`, and runs with the real Massive or Pushover keys.
