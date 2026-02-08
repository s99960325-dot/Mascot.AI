import asyncio
from typing import AsyncGenerator

import httpx

from app.config.setting import settings


class AIService:
    """简单的模型适配服务（MVP）。

    说明：这里实现了对 OpenAI Chat Completions 的示例调用（同步与流式）。
    生产中请抽象适配器与错误/重试/熔断策略。
    """

    OPENAI_URL = "https://api.openai.com/v1/chat/completions"

    async def call_completion(self, body: dict) -> dict:
        """同步调用模型，返回完整响应 JSON"""
        headers = {"Authorization": f"Bearer {settings.OPENAI_API_KEY}"}
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(self.OPENAI_URL, json=body, headers=headers)
            resp.raise_for_status()
            return resp.json()

    async def stream_completion(self, body: dict) -> AsyncGenerator[str, None]:
        """流式调用第三方并逐块 yield 文本片段（字符串）。"""
        # 将流式开关传给下游
        body = dict(body)
        body["stream"] = True

        headers = {"Authorization": f"Bearer {settings.OPENAI_API_KEY}"}

        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("POST", self.OPENAI_URL, json=body, headers=headers) as resp:
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    if not line:
                        continue
                    # OpenAI stream 格式通常为 'data: {...}' 或 'data: [DONE]'
                    if line.startswith("data: "):
                        payload = line.removeprefix("data: ")
                        if payload.strip() == "[DONE]":
                            break
                        # 解析可能的 JSON，简单转发原始字符串为 MVP
                        yield payload
                    else:
                        yield line
                    # 防止单一请求阻塞过久，可做心跳
                    await asyncio.sleep(0)
