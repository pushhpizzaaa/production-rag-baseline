# Reusing Async HTTPX Clients in Dependencies

**Doc ID:** `fastapi_async_httpx_client_in_dependencies`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Maintain persistent HTTP connection pools across route requests using httpx.AsyncClient.

---

## Connection Pooling with AsyncClient
```python
import httpx
from fastapi import FastAPI, Depends
from typing import AsyncGenerator

app = FastAPI()

async def get_http_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    async with httpx.AsyncClient(timeout=10.0) as client:
        yield client

@app.get("/proxy-fetch")
async def proxy_fetch(client: httpx.AsyncClient = Depends(get_http_client)):
    resp = await client.get("https://httpbin.org/get")
    return resp.json()
```

