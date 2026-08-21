# Workflow Studio

[English](README.md)

Workflow Studio 是一个用于构建 Coze 风格可视化、代码化 AI 工作流的全栈项目基础。**Workflow 是第一公民，也是顶层执行抽象**；Agent 仅是由 Workflow 驱动的一种应用形态；画布节点只是 Workflow 中的执行步骤。因此项目中不会有 `AgentNode` 或 `SubAgentNode`。

## 项目能力

- 基于 Vue 3 与 Vue Flow 的可视化工作流画布，支持 8 类节点、配置面板和撤销/重做。
- 由前端、校验器、编译器和运行时共同使用的独立 Workflow DSL。
- FastAPI、SQLAlchemy 2 异步模型、Alembic、MySQL、Redis 的后端基础设施。
- 使用 LangGraph 将 DSL 编译为依赖图，实现静态 Fan-out / Fan-in；`Join(mode="all")` 是汇聚节点。
- 使用 LangChain 抽象 LLM 和 Tool，并提供工厂与注册表扩展点。
- 运行时事件、SSE 流式接口和前端调试时间线。
- 初始登录/注册、工作流可见性与审核状态数据模型，为“我的 Workflows”“Workflow 广场”“发布审核”提供基础。

## 架构

```text
Vue Flow Canvas + Pinia
        |
        | Workflow DSL
        v
FastAPI API -> Service -> Repository -> MySQL
        |
        +-> Validator -> Graph Analyzer -> LangGraph Compiler
                                           |
                                           v
                              Runtime / Node Registry / Event Bus
                                           |
                 LLM Factory / Tool Registry / Knowledge / Code
                                           |
                                           v
                                  SSE -> Debug Panel
```

画布只描述节点和边，不在前端自行调度并发。`WorkflowCompiler` 将边编译为 LangGraph 依赖，LangGraph 负责并行分支与前置依赖等待。

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

`AgentState` 使用 reducer 累积并发节点产生的执行字段；节点只返回局部更新，不直接修改共享状态。`JoinNode` 用于明确表达“所有前置分支完成后再继续”。

## 目录与模块

| 路径 | 职责 |
| --- | --- |
| `backend/app/api` | 认证、Workflow、Run、Tool、Model、健康检查 API。 |
| `backend/app/core` | 配置、常量、结构化日志与敏感字段脱敏。 |
| `backend/app/db` | SQLAlchemy 异步连接、基础模型和数据库实体。 |
| `backend/app/schemas` | Pydantic v2 请求/响应及 Workflow DSL 数据契约。 |
| `backend/app/repositories` | 数据库访问层。 |
| `backend/app/services` | 应用用例层，使 API 不直接依赖数据库或运行时。 |
| `backend/app/compiler` | 图校验、可达性/循环分析、并行组发现和 LangGraph 编译。 |
| `backend/app/runtime` | 状态、事件、事件总线、SSE 与 Workflow 执行器。 |
| `backend/app/nodes` | Start、LLM、Tool、Condition、Code、Knowledge、Join、End 插件节点。 |
| `backend/app/llm` | OpenAI 兼容、Qwen、DeepSeek、Ollama、vLLM 的统一工厂。 |
| `backend/app/tools` | LangChain 工具注册表与内置示例工具。 |
| `backend/app/template` | 安全的 `{{ variable }}` 模板解析，不使用 `eval`。 |
| `frontend/src` | Vue Flow 画布、节点组件、面板、Pinia Store、路由和 API 客户端。 |
| `backend/tests` | DSL、编译器、节点、运行时、API 的测试骨架。 |

## 节点说明

| 节点 | 作用 |
| --- | --- |
| `start` | 注入工作流输入。 |
| `llm` | 渲染提示词，通过 `LLMFactory` 调用模型。 |
| `tool` | 解析参数并调用已注册的 LangChain Tool。 |
| `condition` | 用受限 AST 计算表达式，不使用 `eval`/`exec`。 |
| `code` | 委托给代码执行器接口；默认 Mock 不会在 FastAPI 进程执行用户代码。 |
| `knowledge` | 调用检索器抽象；首期使用 MockRetriever。 |
| `join` | 并发汇聚节点，首期仅支持 `all`。 |
| `end` | 返回最终聚合输出。 |

## Workflow DSL 示例

```json
{
  "version": "1.0",
  "nodes": [
    {"id":"start","type":"start","position":{"x":80,"y":180},"config":{}},
    {"id":"research","type":"llm","position":{"x":320,"y":100},"config":{"provider":"openai","model":"gpt-4o-mini","prompt":"Research: {{ input }}"}},
    {"id":"tool","type":"tool","position":{"x":320,"y":280},"config":{"tool_name":"demo_tool","arguments":{"input":"{{ input }}"}},
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

Validator 会在编译前检查 Start/End、节点 ID、节点类型、边引用、Condition/Join 配置、可达性与循环。

## API

| 分类 | 主要接口 |
| --- | --- |
| 认证 | `POST /api/auth/register`、`POST /api/auth/login` |
| Workflow | 创建、读取、校验、运行、SSE、版本和发布接口位于 `/api/workflows` |
| Run | `GET /api/runs/{run_id}`、`GET /api/runs/{run_id}/nodes` |
| 目录 | `GET /api/tools`、`GET /api/models` |

SSE 地址为 `GET /api/workflows/{workflow_id}/runs/{run_id}/stream`，事件包含工作流、节点、LLM、Tool、Condition 与 Join 生命周期。

## 登录、发布与 Workflow 广场

`users` 表保存账号、密码哈希和角色；`workflows` 表拥有 `owner_id`、`visibility`、`review_status` 字段。目标产品流程为：

1. 登录用户在“我的 Workflows”维护私有工作流。
2. 用户提交发布申请，工作流进入审核状态。
3. 管理员审核通过或驳回。
4. 审核通过的 Workflow 在“Workflow 广场”向所有用户可见。

基础数据结构和认证接口已经具备。完整上线前还需补齐归属校验、审核队列 API、管理员 RBAC、广场查询 API 与对应前端页面。

## 安装与运行

需要 Python 3.12+、Node.js 20+、`uv`；完整运行需要 MySQL 8+ 与 Redis 7+。

```bash
cp .env.example .env
cd backend && uv sync
cd ../frontend && npm install
```

基础设施：`docker compose up mysql redis`。

数据库迁移：`cd backend && uv run alembic upgrade head`。

后端开发：`uv run uvicorn app.main:app --reload`；前端开发：`npm run dev`。

## 扩展开发

- 新节点：继承 `BaseNode`，使用 `register_node()` 注册。
- 新工具：创建 LangChain Tool 并加入 `TOOL_REGISTRY`。
- 新模型提供商：实现适配器后交由 `LLMFactory` 路由。
- 检索器：实现 `KnowledgeRetriever`，可接入 FAISS、Chroma、Milvus、Elasticsearch。
- 代码沙箱：替换 `MockCodeExecutor`，接入 Docker、E2B、Daytona 或托管沙箱。

## 当前范围

本仓库是生产级的项目基础，而非已经上线的托管服务。模块边界和运行时架构已创建；生产部署前仍应补齐 Run/NodeRun 的完整持久化、端到端 LLM token 流、条件边路由、完整审核/RBAC API 和 Workflow 广场页面。
