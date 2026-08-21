# Workflow Studio

[简体中文](README-zh.md)

Workflow Studio is a full-stack foundation for visual, code-first AI workflow orchestration. **Workflow is the first-class execution abstraction**; an Agent is only an optional application form backed by a Workflow. There is intentionally no `AgentNode` or `SubAgentNode`.

## What It Provides

- Vue 3 visual canvas based on Vue Flow, with an eight-node palette and undo/redo history.
- A versioned Workflow DSL shared by the canvas, validation, compiler and runtime.
- FastAPI API, SQLAlchemy 2 async persistence model, Alembic migration baseline, MySQL and Redis Compose services.
- LangGraph compilation for graph dependencies, including static fan-out and fan-in; `Join(mode="all")` is the convergence node.
- LangChain-based LLM and Tool abstractions with provider and registry extension points.
- Runtime event model and SSE endpoint for execution timelines and streamed LLM events.
- Initial account/login data model and APIs, plus workflow visibility and review-status fields for private workflows, publishing and a future moderated public gallery.

## Architecture

```text
Vue Flow Canvas + Pinia
        |
        | Workflow DSL (nodes, edges, config)
        v
FastAPI API -> Services -> Repositories -> MySQL
        |
        +-> Validator -> Graph Analyzer -> LangGraph Compiler
                                           |
                                           v
                              Runtime / Node Registry / Event Bus
                                           |
                  +------------------------+-----------------------+
                  v                        v                       v
               LLM Factory             Tool Registry       Knowledge / Code
                  |
                  v
             SSE stream -> Debug Panel
```

### Execution Model

The canvas never schedules work itself. It describes directed dependencies. `WorkflowCompiler` translates those edges to LangGraph edges, letting LangGraph execute independent branches concurrently and hold a downstream node until all predecessors complete.

```text
                 Start
                   |
          +--------+--------+
          v        v        v
        LLM 1    LLM 2     Tool
          |        |        |
          +--------+--------+
                   v
              Join (all)
                   |
                 LLM 3
                   |
                  End
```

`AgentState` uses append reducers for accumulated execution fields. Node functions return partial updates; they do not mutate shared state. `JoinNode` represents an explicit all-predecessor synchronization point.

## Repository Layout

| Path | Responsibility |
| --- | --- |
| `backend/app/api` | HTTP routes for auth, agents, workflows, runs, tools, models and health. |
| `backend/app/core` | Settings, constants, structured logging and sensitive-value redaction. |
| `backend/app/db` | Async SQLAlchemy engine, declarative base and persistence entities. |
| `backend/app/schemas` | Pydantic v2 request, response and Workflow DSL contracts. |
| `backend/app/repositories` | Persistence access layer. |
| `backend/app/services` | Application use cases, isolating APIs from persistence/runtime details. |
| `backend/app/compiler` | Validation, reachability analysis, cycle detection, parallel group discovery and LangGraph compilation. |
| `backend/app/runtime` | Execution state, events, event bus, SSE and workflow executor. |
| `backend/app/nodes` | Plugin-style implementations for Start, LLM, Tool, Condition, Code, Knowledge, Join and End. |
| `backend/app/llm` | Provider-neutral LLM factory for OpenAI-compatible, Qwen, DeepSeek, Ollama and vLLM endpoints. |
| `backend/app/tools` | LangChain Tool registry and built-in example tool. |
| `backend/app/template` | Safe `{{ variable }}` resolution and rendering without `eval`. |
| `frontend/src` | Vue Flow canvas, node components, panels, stores, views, routing and HTTP client. |
| `backend/tests` | Unit and contract-test scaffold for DSL, compiler, templates, nodes, runtime and API. |
| `docker-compose.yml` | Optional MySQL 8 and Redis 7 infrastructure. |

## Canvas Nodes

| Node | Responsibility |
| --- | --- |
| `start` | Publishes the initial workflow input. |
| `llm` | Renders prompts, delegates model creation to `LLMFactory`, and returns model output. |
| `tool` | Resolves configured arguments and invokes a registered LangChain tool. |
| `condition` | Evaluates a restricted AST expression; never uses `eval` or `exec`. |
| `code` | Delegates to a code-executor interface. The default mock never executes user code in FastAPI. |
| `knowledge` | Queries the retriever abstraction. The default is a mock retriever. |
| `join` | Explicit fan-in point. The first release accepts only `mode: all`. |
| `end` | Produces the terminal aggregate output. |

## Workflow DSL

```json
{
  "version": "1.0",
  "nodes": [
    {"id":"start","type":"start","position":{"x":80,"y":180},"config":{}},
    {"id":"research","type":"llm","position":{"x":320,"y":100},"config":{"provider":"openai","model":"gpt-4o-mini","prompt":"Research: {{ input }}"}},
    {"id":"tool","type":"tool","position":{"x":320,"y":280},"config":{"tool_name":"demo_tool","arguments":{"input":"{{ input }}"}}},
    {"id":"join","type":"join","position":{"x":560,"y":180},"config":{"mode":"all"}},
    {"id":"end","type":"end","position":{"x":760,"y":180},"config":{}}
  ],
  "edges": [
    {"id":"e1","source":"start","target":"research"},
    {"id":"e2","source":"start","target":"tool"},
    {"id":"e3","source":"research","target":"join"},
    {"id":"e4","source":"tool","target":"join"},
    {"id":"e5","source":"join","target":"end"}
  ]
}
```

The validator checks start/end presence, IDs, node types, edge references, condition/join configuration, reachability and cycles before a run is compiled.

## API Surface

| Area | Endpoints |
| --- | --- |
| Auth | `POST /api/auth/register`, `POST /api/auth/login` |
| Agents | `POST /api/agents`, `GET /api/agents`, `GET /api/agents/{id}` |
| Workflows | create, fetch, validate, run, stream, list versions and publish under `/api/workflows` |
| Runs | `GET /api/runs/{run_id}`, `GET /api/runs/{run_id}/nodes` |
| Catalogs | `GET /api/tools`, `GET /api/models` |

The stream route is `GET /api/workflows/{workflow_id}/runs/{run_id}/stream`. Events include workflow, node, LLM, tool, condition and join lifecycle messages.

## Accounts, Publishing and Gallery

`users` stores account credentials and roles. `workflows` has `owner_id`, `visibility` and `review_status` fields. The intended product flow is:

1. A signed-in user works in **My Workflows** (`visibility=private`).
2. The user requests publication; the workflow enters a review state.
3. An administrator approves or rejects it.
4. Approved workflows become visible in the **Workflow Gallery**.

The base schema and auth endpoints are present. Dedicated ownership enforcement, review queue routes and gallery browsing routes are the next application-layer work required to complete moderation.

## Setup

Prerequisites: Python 3.12+, Node.js 20+, `uv`, MySQL 8+ and Redis 7+ for full runtime use.

```bash
cp .env.example .env
cd backend && uv sync
cd ../frontend && npm install
```

Run infrastructure with `docker compose up mysql redis`; apply schema with `cd backend && uv run alembic upgrade head`. Development commands are `uv run uvicorn app.main:app --reload` and `npm run dev`.

## Configuration

`.env.example` documents `DATABASE_URL`, `REDIS_URL`, model provider keys/base URLs and default model selection. Never commit real API keys.

## Extension Points

- **Node:** implement `BaseNode`, then register it through `register_node()`.
- **Tool:** build a LangChain tool and add it to `TOOL_REGISTRY`.
- **Model provider:** add a factory adapter and route it through `LLMFactory`.
- **Retriever:** implement `KnowledgeRetriever` for FAISS, Chroma, Milvus, Elasticsearch or another backend.
- **Code sandbox:** replace `MockCodeExecutor` with Docker, E2B, Daytona or a managed sandbox implementation.

## Quality Gates

Tests live in `backend/tests` and cover validator, graph analyzer, compiler, templates, conditions, node contracts, runtime and API contracts. Execute them with `cd backend && uv run pytest` after configuring the runtime.

## Current Scope

This repository is a production-oriented foundation rather than a finished hosted service. The runtime architecture and module boundaries are implemented; persistence of individual `Run`/`NodeRun` lifecycle records, full streamed token propagation, condition-edge routing, complete RBAC/review APIs and a finished public gallery should be completed before production deployment.
