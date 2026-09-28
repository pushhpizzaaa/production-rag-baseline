# Liveness and Readiness Probes for Kubernetes

**Doc ID:** `fastapi_zero_downtime_deployment_healthchecks`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Implement robust health check endpoints distinguishing liveness from readiness probes.

---

## Kubernetes Health Checks
- **Liveness (`/healthz`)**: Verifies if the process is alive. If this fails, container runtime restarts the container.
- **Readiness (`/ready`)**: Verifies if dependencies (DB, vectorstore) are ready to accept traffic.

```python
from fastapi import FastAPI, Response, status

app = FastAPI()

@app.get("/healthz", status_code=status.HTTP_200_OK)
def liveness():
    return {"status": "alive"}

@app.get("/ready")
def readiness(response: Response):
    db_connected = True # check DB connection
    vector_ready = True # check Qdrant ping
    if not (db_connected and vector_ready):
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "unhealthy", "db": db_connected, "vector": vector_ready}
    return {"status": "ready"}
```

