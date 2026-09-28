# OpenAPI Metadata and Docs URL Customization

**Doc ID:** `fastapi_metadata_docs_urls_openapi_customization`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Customize Swagger UI path, ReDoc URL, OpenAPI schema version, and licensing information.

---

## Customizing Interactive Documentation
```python
from fastapi import FastAPI

app = FastAPI(
    title="Core Banking API",
    description="High-security REST API for accounts and transactions.",
    version="2.4.0",
    docs_url="/api/docs",        # Swagger UI custom URL (or None to disable)
    redoc_url="/api/redoc",      # ReDoc custom URL
    openapi_url="/api/v1/openapi.json",
    contact={"name": "Platform Engineering", "email": "platform@bank.internal"}
)
```

