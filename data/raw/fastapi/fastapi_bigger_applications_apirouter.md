# Modular Applications with APIRouter

**Doc ID:** `fastapi_bigger_applications_apirouter`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Structure large multi-file FastAPI projects into modular domain routers with prefix and tag controls.

---

## Structuring Large Projects
Organize your codebase into routers:

```python
# routers/users.py
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
async def list_users():
    return [{"username": "alice"}]

# main.py
from fastapi import FastAPI
# from routers import users

app = FastAPI(title="Modular System")
app.include_router(router)
```
Prefixes, dependencies, and tags applied in `include_router` propagate to all endpoints within that router.

