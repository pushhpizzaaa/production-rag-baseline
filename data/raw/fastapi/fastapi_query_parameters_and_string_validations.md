# Query Parameters and String Validations

**Doc ID:** `fastapi_query_parameters_and_string_validations`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Query parameters are key-value pairs passed in the URL after a question mark, used for filtering, pagination, and sorting.

---

## Declaring Query Parameters
Function parameters that are not part of path parameters are automatically interpreted as query parameters:

```python
from typing import Annotated
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items/")
async def read_items(
    q: Annotated[str | None, Query(min_length=3, max_length=50, pattern="^[a-zA-Z0-9_-]+$")] = None,
    skip: Annotated[int, Query(ge=0, description="Offset for pagination")] = 0,
    limit: Annotated[int, Query(gt=0, le=100, description="Page limit")] = 10,
):
    return {"q": q, "skip": skip, "limit": limit}
```

### Validation Constraints with Query()
- `min_length`, `max_length`: String length boundaries.
- `pattern`: Regular expression for regex verification.
- `ge`, `gt`, `le`, `lt`: Numeric comparisons (greater/less than or equal).
- `deprecated=True`: Flags parameter as deprecated in Swagger UI.
- `alias`: Use alternative query parameter name (e.g. `item-query`).

### Query Parameter Lists / Multiple Values
```python
@app.get("/search/")
async def search(tags: Annotated[list[str] | None, Query()] = None):
    return {"tags": tags or []}
```
Client query: `/search/?tags=python&tags=fastapi` yields `tags: ["python", "fastapi"]`.

