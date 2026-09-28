# API Key Authentication via Headers or Query Parameters

**Doc ID:** `fastapi_openapi_security_schemes_api_key`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Secure endpoints using static API keys extracted via APIKeyHeader or APIKeyQuery.

---

## APIKeyHeader Pattern
```python
from fastapi import FastAPI, Security, HTTPException, status
from fastapi.security import APIKeyHeader

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)
VALID_API_KEY = "sk-prod-98721634"

app = FastAPI()

def require_api_key(api_key: str = Security(API_KEY_HEADER)):
    if api_key != VALID_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate API key"
        )
    return api_key

@app.get("/protected", dependencies=[Security(require_api_key)])
def protected_route():
    return {"access": "granted"}
```

