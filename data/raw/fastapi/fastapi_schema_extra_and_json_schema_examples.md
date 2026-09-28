# JSON Schema Extras and OpenAPI Documentation Styling

**Doc ID:** `fastapi_schema_extra_and_json_schema_examples`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Annotate Pydantic models with rich metadata to customize Swagger schema documentation.

---

## Configuring Schema Extra
```python
from pydantic import BaseModel, ConfigDict
from fastapi import FastAPI

class SystemStatus(BaseModel):
    service_name: str
    uptime_seconds: int
    healthy: bool

    model_config = ConfigDict(
        json_schema_extra={
            "description": "Standardized health check telemetry model",
            "example": {
                "service_name": "rag-retrieval-service",
                "uptime_seconds": 86400,
                "healthy": True
            }
        }
    )
```

