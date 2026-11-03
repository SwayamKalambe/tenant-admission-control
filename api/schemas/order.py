"""Request and response schemas for orders."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class OrderCreate(BaseModel):
    item_name: str = Field(min_length=1, max_length=200)
    amount: Decimal = Field(gt=0, max_digits=10, decimal_places=2)


class OrderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tenant_id: int
    item_name: str
    amount: Decimal
    created_at: datetime
