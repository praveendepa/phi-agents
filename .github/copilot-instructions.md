# Copilot instructions for phi-agents

This file gives actionable, repo-specific guidance for AI coding agents working on phi-agents.

## Purpose
- Help contributors (and AI assistants) quickly understand the architecture, workflows, and conventions used here so edits and feature work are consistent and productive.

## Big picture
- Core code lives under [src/phi_agents](src/phi_agents). The project composes multiple small "Agent" factories (in `src/phi_agents/functions`) and wires them into a team in [src/phi_agents/run_agents.py](src/phi_agents/run_agents.py).
- Two user-facing entry points: a Streamlit frontend at `run_agents.py` and a FastAPI endpoint at [src/phi_agents/app/my-mainapp.py](src/phi_agents/app/my-mainapp.py).
- The repo relies on the `agno` framework: agents, tools, and model wrappers are instantiated via `agno.agent.Agent` and `agno.models.*` implementations.

## Key files to inspect
- [config.json](config.json) — environment-specific DB settings. Code reads `ENV` from the environment to choose `local` vs `cloud` entries.
- [src/phi_agents/run_agents.py](src/phi_agents/run_agents.py) — example of building an Agent team, streaming responses, and Streamlit UI integration.
- [src/phi_agents/app/my-mainapp.py](src/phi_agents/app/my-mainapp.py) — FastAPI wrapper for the SQL agent (run with `uvicorn` as shown in the comment).
- `src/phi_agents/functions/*` — individual agent factories (e.g., `web_search.py`, `finance_agent.py`, `api_calls.py`, `sql_agent.py`, `browser_task_agent.py`). These functions return configured `Agent` instances.
- [src/phi_agents/requirements.txt](src/phi_agents/requirements.txt) — runtime dependencies (notably `agno`, `openai`, `streamlit`, `fastapi`, `sqlalchemy`).

## Project-specific patterns and conventions
- Agent factories: each file in `functions/` exposes a function that returns an `Agent` (e.g., `def web_agent(): return Agent(...)`). Follow this pattern when adding new agents.
- Model selection: agents are constructed with `agno.models.*` wrappers. Multiple model options are present but commented; change the `model=...` line in the agent factory to switch models.
- Tools: agent capabilities are attached via `tools=[...]` (examples: `DuckDuckGoTools()`, `YFinanceTools()`, `CustomApiTools(...)`, `BrowserTools()`). When adding a tool, mirror existing patterns in `functions/`.
- Streaming: code uses `agent.run(question, stream=True)` and iterates returned chunks (see `run_agents.py` and `my-mainapp.py`). Preserve this streaming pattern when modifying response handling.
- Agent team: `Agent(..., team=[...], instructions=[...], show_tool_calls=True, markdown=True)` — team-level `instructions` and `show_tool_calls` are used throughout; beware changing these flags.

## Environment & runtime
- Check for existing virtual environments first & use the appropriate env. If not present, create a new one and install dependencies from `requirements.txt`.
- Required files: `config.json` (DB hosts/credentials) and an `.env` file for secrets like `HF_TOKEN` or model API keys. `ENV` environment variable chooses the config block (`local` or `cloud`).
- Start Streamlit UI (from repo root):

```bash
pip install -r src/phi_agents/requirements.txt
streamlit run src/phi_agents/run_agents.py --server.port 8501
```

- Start FastAPI app (commented hint in `my-mainapp.py`):

```bash
uvicorn src.phi_agents.app.my-mainapp:app --env-file .env --reload
```

- Load F1 sample data into the DB (uses `agents.db_url`):

```bash
python src/phi_agents/functions/load_f1_data.py
```

## Integration points & external dependencies
- Database: `config.json` and `agents.db_url` (used by `load_f1_data.py`). The SQL agent expects a running PostgreSQL instance matching the `config.json` settings.
- External APIs / models: API keys and tokens are read from environment variables (e.g., `HF_TOKEN`, OpenAI keys). The repo depends on third-party packages in `requirements.txt`.
- Internal HTTP call: `api_calls.py` demonstrates a `CustomApiTools` usage pointing at `my-sql-api` (FastAPI). Keep host/port consistent with where FastAPI is deployed.

## Editing & testing guidance for AI agents
- When modifying or adding agents, follow the existing small-function factory pattern and keep `show_tool_calls`/`markdown` flags consistent.
- To test agent behavior locally, prefer the Streamlit UI for quick manual trials and the FastAPI endpoint for automated or programmatic checks.
- Preserve streaming iteration logic when changing `Agent.run` usage — several parts of the code expect chunked responses.

## Examples (copy-paste friendly)
- Create a new agent factory in `src/phi_agents/functions/new_agent.py` that returns an `Agent` instance with `name`, `role`, `model`, and optional `tools`.
- Wire it into the team in `run_agents.py` by importing and adding it into the `Agent(..., team=[...])` list.

---
If anything here is unclear or you want more detail (e.g., specific model env var names, CI/run scripts, or more file links), tell me which areas to expand and I'll iterate.
