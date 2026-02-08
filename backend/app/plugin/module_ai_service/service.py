from typing import List


class AIAdminService:
    async def list_providers(self) -> List[dict]:
        # MVP 返回静态示例，后续接入数据库查询
        return [
            {"id": "openai", "name": "OpenAI", "status": "available"},
            {"id": "anthropic", "name": "Anthropic", "status": "unknown"},
        ]
