# GZip Middleware for Response Compression

**Doc ID:** `fastapi_middleware_gzip_compression`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Compress HTTP responses exceeding a size threshold to reduce bandwidth consumption and latency.

---

## Enabling GZip Compression
```python
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI()

# Automatically compress responses larger than 1000 bytes
app.add_middleware(GZipMiddleware, minimum_size=1000)

@app.get("/large-data")
async def get_large_payload():
    return {"data": ["heavy_record" for _ in range(5000)]}
```

