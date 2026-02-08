from fastapi import APIRouter, HTTPException

from app.core.router_class import OperationLogRoute

from .service import AIAdminService


AdminRouter = APIRouter(route_class=OperationLogRoute, prefix="/admin/ai_service", tags=["AI 管理"])


@AdminRouter.get("/health", summary="AI 管理 - 健康检查")
async def health_check():
    try:
        return {"ok": True, "service": "module_ai_service"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@AdminRouter.get("/providers", summary="列出模型提供商")
async def list_providers():
    return await AIAdminService().list_providers()
