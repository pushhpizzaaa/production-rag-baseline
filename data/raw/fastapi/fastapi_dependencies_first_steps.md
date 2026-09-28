# Dependency Injection: First Steps

**Doc ID:** `fastapi_dependencies_first_steps`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** FastAPI features a built-in Dependency Injection system using Depends for code reuse and shared logic.

---

## Introduction to Depends
Dependency Injection allows declaring reusable logic (such as authentication, database sessions, query parameters) that FastAPI executes automatically before the route handler:

```python
from typing import Annotated
from fastapi import FastAPI, Depends

app = FastAPI()

async def common_pagination(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(pagination: Annotated[dict, Depends(common_pagination)]):
    return {"data": [], "pagination": pagination}

@app.get("/users/")
async def read_users(pagination: Annotated[dict, Depends(common_pagination)]):
    return {"users": [], "pagination": pagination}
```

### Benefits
- Eliminate duplicated validation and parameter parsing code.
- Simplifies unit testing via `app.dependency_overrides`.
- Clean separation of business logic from transport concerns.

