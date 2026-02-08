from sqlalchemy import Integer, String, Text, DateTime, ForeignKey
from app.core.base_model import ModelMixin, mapped_column


class ApiKeyModel(ModelMixin):
    __tablename__ = "api_key"

    key: mapped_column = mapped_column(String(128), nullable=False, unique=True, index=True, comment="API Key")
    customer_id: mapped_column = mapped_column(Integer, ForeignKey("customer.id"), nullable=True, index=True)


class ModelProviderModel(ModelMixin):
    __tablename__ = "model_provider"

    name: mapped_column = mapped_column(String(64), nullable=False, index=True)
    code: mapped_column = mapped_column(String(64), nullable=False, unique=True, index=True)


class UsageLogModel(ModelMixin):
    __tablename__ = "usage_log"

    customer_id: mapped_column = mapped_column(Integer, nullable=False, index=True)
    model: mapped_column = mapped_column(String(128), nullable=False)
    cost: mapped_column = mapped_column(String(64), nullable=True)
