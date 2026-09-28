# API Rate Limiting with SlowAPI

**Doc ID:** `fastapi_rate_limiting_slowapi`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Protect endpoints from DDoS and quota abuse using IP or user-based token bucket rate limiters.

---

## Rate Limiting with SlowAPI
```python
from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/throttled")
@limiter.limit("5/minute")
async def throttled_route(request: Request):
    return {"message": "You are within rate limits"}
```

