# Application Lifespan Events and Startup/Shutdown

**Doc ID:** `fastapi_events_lifespan_handlers`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Manage connection pools and machine learning model preloading using the modern lifespan async context manager.

---

## Lifespan Context Manager
`lifespan` replaces the deprecated `@app.on_event("startup")` and `@app.on_event("shutdown")`:

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load ML models or initialize DB pools
    print("Preloading embedding models...")
    ml_models["model"] = "loaded_weights"
    yield
    # Shutdown: Release resources
    print("Releasing database connection pools...")
    ml_models.clear()

app = FastAPI(lifespan=lifespan)
```

