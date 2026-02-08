from typing import AsyncGenerator

from fastapi import APIRouter, Body, Request, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse

from app.core.router_class import OperationLogRoute
from app.api.v1.module_ai.chat.service import AIService


ChatRouter = APIRouter(route_class=OperationLogRoute, prefix="/chat", tags=["AI"])


@ChatRouter.post(
    "/completions",
    summary="对外 - 聊天完成（支持同步与流式 SSE）",
)
async def chat_completions(request: Request, body: dict = Body(...)):
    """
    支持两种模式：
    - 同步（默认）：返回完整 JSON
    - 流式：当请求带 `stream=true` 查询参数或客户端 `Accept: text/event-stream` 时，以 SSE 方式逐块返回
    """
    # 判断是否客户端想要流式
    query = dict(request.query_params)
    want_stream = query.get("stream") == "true" or request.headers.get("accept", "").find("text/event-stream") != -1

    if want_stream:
        async def event_generator() -> AsyncGenerator[bytes, None]:
            try:
                async for chunk in AIService().stream_completion(body=body):
                    # 每个 chunk 外层按 SSE 格式发送
                    yield f"data: {chunk}\n\n".encode("utf-8")
                # 结束事件
                yield b"event: done\ndata: [DONE]\n\n"
            except Exception as e:
                yield f"event: error\ndata: {str(e)}\n\n".encode("utf-8")

        return StreamingResponse(event_generator(), media_type="text/event-stream")

    # 同步返回（合并完整结果）
    try:
        result = await AIService().call_completion(body=body)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
