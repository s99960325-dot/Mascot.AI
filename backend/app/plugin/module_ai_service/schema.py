from pydantic import BaseModel
from typing import Optional


class ProviderOut(BaseModel):
    id: str
    name: str
    status: Optional[str] = None


class ApiKeyCreate(BaseModel):
    customer_id: int
    description: Optional[str] = None
