
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import getdb
from api.models import Order, Tenant
from api.schemas.order import OrderCreate, OrderRead
from api.admission.controller import check_admission
from api.admission.config import AdmissionConfig

orders_router = APIRouter(tags=["orders"])


@orders_router.post(
    "/tenants/{tenant_id}/orders",
    response_model=list[OrderRead],
    status_code=status.HTTP_201_CREATED
)
def create_order(
    tenant_id: UUID,
    payload: OrderCreate,
    db: Session = Depends(getdb)
):
    tenant = db.query(Tenant).filter(
        Tenant.id == tenant_id
    ).first()

    if tenant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found"
        )

    # Cost-aware admission check for POST
    if not check_admission(
        tenant_id,
        AdmissionConfig.POST_COST
    ):
        raise HTTPException(
            status_code=429,
            detail="Tenant workload limit exceeded"
        )

    orders = []

    # Insert 50 orders per request
    for _ in range(50):
        order = Order(
            tenant_id=tenant_id,
            item_name=payload.item_name,
            amount=payload.amount
        )
        orders.append(order)

    db.add_all(orders)
    db.commit()

    for order in orders:
        db.refresh(order)

    return orders


@orders_router.get(
    "/tenants/{tenant_id}/orders",
    response_model=list[OrderRead]
)
def list_tenant_orders(
    tenant_id: UUID,
    db: Session = Depends(getdb)
):
    tenant = db.query(Tenant).filter(
        Tenant.id == tenant_id
    ).first()

    if tenant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found"
        )

    # Cost-aware admission check for GET
    if not check_admission(
        tenant_id,
        AdmissionConfig.GET_COST
    ):
        raise HTTPException(
            status_code=429,
            detail="Tenant workload limit exceeded"
        )

    orders = (
        db.query(Order)
        .filter(Order.tenant_id == tenant_id)
        .order_by(Order.created_at.desc())
        .limit(100)
        .all()
    )

    return orders
