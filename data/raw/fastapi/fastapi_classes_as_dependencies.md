# Classes as Dependencies

**Doc ID:** `fastapi_classes_as_dependencies`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Use Python classes as dependencies to combine stateful initialization and type inference cleanly.

---

## Class-Based Dependencies
Instead of functions, classes can serve as dependencies. FastAPI automatically invokes `__init__`:

```python
from typing import Annotated
from fastapi import FastAPI, Depends

app = FastAPI()

class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 50):
        self.q = q
        self.skip = skip
        self.limit = limit

@app.get("/products/")
async def list_products(params: Annotated[CommonQueryParams, Depends()]):
    # When Depends() has no arguments, FastAPI infers the class from type hint
    return {"query": params.q, "offset": params.skip, "limit": params.limit}
```

