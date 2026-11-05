# Trading Floor

Four AI traders (Warren, George, Ray, Cathie) trade a simulated account through MCP servers
(accounts, market data, push notifications), each backed by a researcher sub-agent
(fetch, Tavily search, memory). A Gradio dashboard shows the floor live.

All four traders default to `gpt-6-sol`. Set `USE_MANY_MODELS=true` to give each a different provider's model.

## Run
```bash
cp .env.example .env   # add your keys
uv sync
uv run app.py          # dashboard
```
Needs `uv` and `npx` on PATH (the MCP servers launch through them). The optional `frontend/`
is a Vite app: `cd frontend && npm install && npm run dev`.
