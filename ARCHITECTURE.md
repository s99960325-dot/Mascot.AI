# 系统架构概要（基于 FastapiAdmin 构建第三方大模型 API 服务与管理平台）

摘要
- 系统定位：企业级 SaaS 平台，统一接入并管理第三方大模型 API，对外提供稳定、可观测、可计费的模型服务接口。
- 核心目标：高并发、低延迟、流式响应能力、细粒度权限与计费、运营可视化。
- 技术基线：FastAPI（服务层）、FastapiAdmin（管理后台）、httpx（异步模型调用）、Redis（缓存/限流）、PostgreSQL（持久化）、SSE（流式返回）、Kong/APISIX（网关）、Prometheus/Grafana（监控）。

组件与推荐技术

| 组件 | 推荐技术 | 第三方 API 特定配置 / 考量 |
|---|---|---|
| API 网关 | Kong / APISIX | 按 API Key 实施不同 QPS 限制；对接上游厂商的速率限制和鉴权机制；下沉鉴权与限流以减轻业务侧负担 |
| 业务框架 | FastAPI | 异步处理外部 HTTP 请求，支持 SSE 流式返回，易与 FastapiAdmin 后端同源集成 |
| 模型抽象层 | 自研适配器模式 | 定义统一适配器接口（prepare_request, call, stream_response, parse_usage），为每家供应商实现独立适配器，封装重试/限速/降级 |
| 提示词引擎 | LangChain / 自研 | 可将高层业务意图转换成供应商特定的最优提示词；建议支持模板和变量替换，并缓存常用提示模板 |
| 缓存 | Redis | 缓存模型生成结果、模型列表、价格等，减少重复调用；用于分布式令牌桶限流与会话上下文临时存储 |
| 数据库 | PostgreSQL | 存储用户、API Key、调用日志、计费记录；建议为 `customer_id`, `created_at`, `status` 建索引以便统计与审计 |
| 任务队列 | Celery / ARQ | 处理异步、批量、长时间生成与审核任务，结合 Redis 作为 broker 或结果存储 |
| 监控 | Prometheus + Grafana | 采集 QPS、延迟、错误率、模型后端延迟与 Token 用量；为每个供应商建立独立面板与告警 |

重要实现要点
- API 验证：使用 API Key（与 FastapiAdmin 的用户体系关联），支持创建、停用、绑定套餐与额度。
- 限流策略：Redis 分布式令牌桶，按客户与路由粒度限速；在 API 网关或应用侧均可实现。
- 流式响应：采用 SSE（或可选 WebSocket），模型适配器将供应商的 chunk 流规范化并转发给客户端。
- 计费与审计：在请求开始记录审计条目，请求结束后更新耗时、状态、消耗（Token/计数），并入账计费子系统。
- 降级与熔断：当主供应商不可用或超时，自动切换到备选供应商或返回用户友好降级信息。

分阶段实施建议
- MVP：实现 `POST /v1/chat/completions`（同步 + SSE），API Key 存储与简单限流，后台可查看 API Key 与调用记录。
- 服务强化：接入多家供应商适配器、计费流水、Redis 分布式限流与缓存、Prometheus 指标埋点。
- 规模化：容器化 + Kubernetes 编排，使用 API Gateway 下沉鉴权/限流，完善监控与 HPA。

工程交付（快速清单）
- 后端插件目录：`backend/app/plugin/module_ai_service/`（包含 `controller.py`, `service.py`, `model.py`, `schema.py`）
- 对外 API 路径：`/v1/chat/completions`（位于 `backend/app/api/v1/module_ai/chat/`）
- 前端管理页：`frontend/src/views/module_system/ai_service/index.vue`，对应 Pinia store `frontend/src/store/modules/ai.store.ts` 和 API 封装 `frontend/src/api/module_system/ai_service.ts`

如需将此文档作为系统提示词的一部分，可将本文件摘要段复制到 system prompt 中，并指定所需的 MVP 优先级与首选供应商（例如 OpenAI）。
