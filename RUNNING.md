运行与快速验证说明（MVP 验证）

准备工作
1. 在项目根目录有 docker-compose.yaml 和 deploy.sh。推荐先确保 Docker & Docker Compose 已安装。
2. 必要环境变量（示例）：

ENVIRONMENT=dev
SERVER_HOST=0.0.0.0
SERVER_PORT=8000

# 第三方模型（MVP 使用 OpenAI）
OPENAI_API_KEY=sk-xxxx

# 数据库与 Redis（docker-compose 会提供服务）
DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/fastapiadmin
REDIS_URL=redis://redis:6379/0

快速启动（Docker Compose）

在仓库根目录执行：

docker-compose up -d --build

验证步骤（MVP）
1. 启动后访问后台和 API 文档（示例）：
   - 后台地址： http://localhost:8000/docs  (根据 settings.DOCS_URL)

2. 示例同步请求（curl）：

curl -X POST "http://localhost:8000/v1/chat/completions" -H "Content-Type: application/json" -d '{"model":"gpt-4","messages":[{"role":"user","content":"你好"}]}'

3. 示例 SSE 流式（使用 curl -N）：

curl -N -H "Accept: text/event-stream" -X POST "http://localhost:8000/v1/chat/completions" -H "Content-Type: application/json" -d '{"model":"gpt-4","messages":[{"role":"user","content":"讲个笑话"}]}'

4. 在后台查看模型提供商列表：登录 FastapiAdmin 后台，进入 “AI 服务管理” 页面（模块管理 -> AI 服务管理），点击刷新。

本地 smoke 测试（快速语法/导入检查）
1. 推荐在虚拟环境中安装 requirements.txt 中声明的依赖后运行单元测试或静态检查。
2. 可用命令（Windows PowerShell）：

python -m pip install -r backend/requirements.txt
python backend/main.py run --env=dev

注意事项
- 如果使用真实 OpenAI Key，请务必做好密钥管理与费用监控。
- 若上游厂商对流式格式或字段有差异，请在 AIService 适配器中实现解析逻辑并标准化输出。
