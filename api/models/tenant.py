from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID

from core import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    status = Column(String(50), nullable=False, default="registered")
    created_at = Column(DateTime(timezone=True), server_default=func.now())