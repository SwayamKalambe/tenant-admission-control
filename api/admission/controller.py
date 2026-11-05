
import time
from threading import Lock

from api.admission.config import AdmissionConfig

tenant_counters = {}
counter_lock = Lock()


def check_admission(tenant_id, request_cost):

    if not AdmissionConfig.ENABLE_COST_AWARE_ADMISSION:
        return True

    current_time = time.monotonic()
    tenant_id = str(tenant_id)

    with counter_lock:

        counter = tenant_counters.get(tenant_id)

        # Start a new one-second window
        if counter is None or current_time - counter["start"] >= 1:
            tenant_counters[tenant_id] = {
                "start": current_time,
                "cost": 0
            }

        counter = tenant_counters[tenant_id]

        # Check whether the request exceeds the workload budget
        if counter["cost"] + request_cost > AdmissionConfig.TENANT_WORKLOAD_LIMIT:
            return False

        # Consume workload units
        counter["cost"] += request_cost

        return True
