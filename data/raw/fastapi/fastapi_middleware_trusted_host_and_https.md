# Trusted Host and HTTPS Redirect Middleware

**Doc ID:** `fastapi_middleware_trusted_host_and_https`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Protect against HTTP Host Header attacks and force HTTPS in production deployments.

---

## Hardening API with Middleware
```python
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

app = FastAPI()

# Enforce valid Host header
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["api.mydomain.com", "*.mydomain.com", "localhost"]
)

# In production, enforce HTTPS redirect
# app.add_middleware(HTTPSRedirectMiddleware)
```

