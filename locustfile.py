import random
from locust import HttpUser, task, between

# TEST_MODE = "POST"
# Tenant IDs
TENANTS = {
    "Tenant 1": "02e98fab-c554-429a-afb2-b881232003ba",
    "Tenant 2": "65c1e7b6-6fe8-4df1-b0bf-572808f5bed9",
    "Tenant 3": "6187df72-394f-4dc4-b6f1-f780e33f96e2",
}


# Available items
ITEMS = {
    1: "Laptop",
    2: "Mouse",
    3: "Keyboard",
    4: "Monitor",
    5: "Headphones",
    6: "USB Cable",
    7: "Webcam",
    8: "Printer",
    9: "External Hard Drive",
    10: "Speaker",
    11: "Smartphone",
    12: "Tablet",
    13: "Charger",
    14: "Power Bank",
    15: "Router",
    16: "Microphone",
    17: "SSD",
    18: "RAM",
    19: "Graphics Card",
    20: "Motherboard"
}


# Base tenant user
class TenantUser(HttpUser):
    abstract = True

    wait_time = between(0.1, 0.5)

    tenant_name = None
    tenant_id = None

    @task
    def create_order(self):

        # if TEST_MODE != "POST":
        #     return

        payload = {
            "item_name": random.choice(list(ITEMS.values())),
            "amount": round(random.uniform(10, 1000), 2)
        }

        self.client.post(
            f"/tenants/{self.tenant_id}/orders",
            json=payload,
            name=f"{self.tenant_name} - Create Order"
        )

    @task
    def list_orders(self):

        # if TEST_MODE != "GET":
        #     return

        self.client.get(
            f"/tenants/{self.tenant_id}/orders",
            name=f"{self.tenant_name} - List Orders"
        )


# Tenant 1
class Tenant1User(TenantUser):
    weight = 1
    tenant_name = "Tenant 1"
    tenant_id = TENANTS["Tenant 1"]


# Tenant 2
class Tenant2User(TenantUser):
    weight = 1
    tenant_name = "Tenant 2"
    tenant_id = TENANTS["Tenant 2"]


# Tenant 3
class Tenant3User(TenantUser):
    weight = 3
    tenant_name = "Tenant 3"
    tenant_id = TENANTS["Tenant 3"]