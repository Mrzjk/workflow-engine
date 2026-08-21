# Agent Platform

Coze-style visual Agent Workflow Canvas. An Agent owns Workflows; it is not a canvas node. The Vue Flow canvas serializes Workflow DSL, validates it, then the FastAPI runtime compiles it to LangGraph. LangGraph dependency edges provide fan-out/fan-in scheduling; Join `mode: all` waits for all incoming branches.

## Structure
`backend/app` contains API, database, schemas, repositories, services, compiler, runtime, nodes, LLM, tools and template modules. `frontend/src` contains Vue Flow canvas, node palette, properties editor, Pinia stores and debug panel.

## Install
Copy `.env.example` to `.env`. Run `cd backend && uv sync`, then `cd ../frontend && npm install`. Start commands are `uv run uvicorn app.main:app --reload` and `npm run dev`. Infrastructure is available through `docker compose up mysql redis`.

## DSL
```json
{"version":"1.0","nodes":[{"id":"start","type":"start","position":{"x":0,"y":0},"config":{}},{"id":"end","type":"end","position":{"x":200,"y":0},"config":{}}],"edges":[{"id":"e1","source":"start","target":"end"}]}
```

## Extending
Register nodes in `app/nodes/registry.py`, tools in `app/tools/registry.py`, and providers through `LLMFactory`. Run migrations with `uv run alembic upgrade head`; tests are under `backend/tests`.
