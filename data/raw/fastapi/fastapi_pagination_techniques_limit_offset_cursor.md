# Pagination Techniques: Limit-Offset vs Cursor-Based

**Doc ID:** `fastapi_pagination_techniques_limit_offset_cursor`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Design scalable pagination schemas supporting traditional offset and high-performance keyset cursor pagination.

---

## Keyset / Cursor Pagination Schema
```python
from pydantic import BaseModel
from typing import Generic, TypeVar
from fastapi import FastAPI

T = TypeVar("T")

class CursorPage(BaseModel, Generic[T]):
    items: list[T]
    next_cursor: str | None
    has_more: bool

app = FastAPI()

@app.get("/feed", response_model=CursorPage[str])
async def get_feed(cursor: str | None = None, limit: int = 20):
    # Keyset query: WHERE id > cursor ORDER BY id LIMIT limit
    items = ["item_a", "item_b"]
    return CursorPage(items=items, next_cursor="item_b", has_more=False)
```

