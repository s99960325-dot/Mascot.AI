from fastapi import APIRouter

from .chat.controller import ChatRouter

# 将对外 API 按 /v1 前缀暴露
api_router = APIRouter(prefix="/v1")

api_router.include_router(ChatRouter)
