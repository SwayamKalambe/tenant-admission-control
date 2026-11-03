"""Tenant and workload API schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, StrictInt


class TenantCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)


class TenantRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    status: str
    created_at: datetime


class WorkloadRequest(BaseModel):
    requests: StrictInt = Field(gt=0, le=100_000)


class WorkloadResult(BaseModel):
    tenant_id: int
    requested_workload: int
    status: str
    execution_time_seconds: float
