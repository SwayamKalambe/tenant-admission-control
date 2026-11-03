from fastapi import FastAPI

from api import (
    orders_router, 
    tenants_router
    )

app = FastAPI(title="Tenant Control Admission")


app.include_router(tenants_router)
app.include_router(orders_router)


@app.get("/")
def cover_page():
    return "Welcome to Tenant Control Admission"
