
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import getdb
from api.models import Order, Tenant
from api.schemas.order import OrderCreate, OrderRead

orders_router = APIRouter(tags=["orders"])


@orders_router.post(
    "/tenants/{tenant_id}/orders",
    response_model=OrderRead,
    status_code=status.HTTP_201_CREATED
)
def create_order(
    tenant_id: int,
    payload: OrderCreate,
    db: Session = Depends(getdb)
):
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()

    if tenant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found"
        )

    order = Order(
        tenant_id=tenant_id,
        item_name=payload.item_name,
        amount=payload.amount
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    return order


@orders_router.get(
    "/tenants/{tenant_id}/orders",
    response_model=list[OrderRead]
)
def list_tenant_orders(
    tenant_id: int,
    db: Session = Depends(getdb)
):
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()

    if tenant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found"
        )

    orders = db.query(Order).filter(
        Order.tenant_id == tenant_id
    ).order_by(Order.id).all()

    return orders
