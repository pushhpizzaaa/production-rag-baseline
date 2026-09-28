# Sub-dependencies and Dependency Composition

**Doc ID:** `fastapi_sub_dependencies_composition`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Compose multiple hierarchical dependencies where dependencies depend on other dependencies.

---

## Hierarchical Dependency Trees
FastAPI automatically resolves recursive dependency trees:

```python
from typing import Annotated
from fastapi import FastAPI, Depends, Header, HTTPException

app = FastAPI()

def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    return x_token

def verify_key(x_key: Annotated[str, Header()], token: Annotated[str, Depends(verify_token)]):
    if x_key != "secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return {"token": token, "key": x_key}

@app.get("/secure-data/")
async def get_secure_data(credentials: Annotated[dict, Depends(verify_key)]):
    return {"status": "authenticated", "credentials": credentials}
```
FastAPI detects that `verify_key` needs `verify_token`, evaluates `verify_token` first, caches its result for the request, and passes it into `verify_key`.

