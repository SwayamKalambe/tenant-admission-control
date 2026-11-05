import uuid
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from core.database import Base


class TenantAdmissionConfig(Base):
    __tablename__ = "tenant_admission_configs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)

    initial_limit = Column(Float, nullable=False)
    min_limit = Column(Float, nullable=False)
    max_limit = Column(Float, nullable=False)
    current_limit = Column(Float, nullable=False)

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
