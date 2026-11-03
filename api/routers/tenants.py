
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core import getdb
from api.models import Tenant
from api.schemas import TenantCreate, TenantRead

tenants_router = APIRouter(tags=["tenants"])


@tenants_router.post(
    "/register_tenant",
    response_model=TenantRead,
    status_code=status.HTTP_201_CREATED
)
def register_tenant(
    payload: TenantCreate,
    db: Session = Depends(getdb)
):
    tenant = Tenant(
        name=payload.name
    )

    db.add(tenant)
    db.commit()
    db.refresh(tenant)

    return tenant


@tenants_router.get(
    "/list_tenants",
    response_model=list[TenantRead]
)
def list_tenants(db: Session = Depends(getdb)):
    tenants = db.query(Tenant).order_by(Tenant.id).all()

    return tenants


@tenants_router.get(
    "/get_tenant/{tenant_id}",
    response_model=TenantRead
)
def get_tenant(
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

    return tenant
