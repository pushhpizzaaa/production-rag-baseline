# Nested Pydantic Models and Complex Attributes

**Doc ID:** `fastapi_body_nested_models`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Construct deeply nested hierarchical JSON schemas with sub-models, sets, and image/file references.

---

## Deeply Nested Models
Pydantic models can nest other models to define clean hierarchical data structures:

```python
from pydantic import BaseModel, HttpUrl
from fastapi import FastAPI

app = FastAPI()

class Image(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tags: set[str] = set()
    images: list[Image] | None = None

class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item]

@app.post("/offers/")
async def create_offer(offer: Offer):
    return {"offer_name": offer.name, "item_count": len(offer.items)}
```

### Self-Referencing and Recursive Models
Pydantic v2 supports recursive self-referential schemas using `from __future__ import annotations` or `model_rebuild()`:
```python
class Category(BaseModel):
    name: str
    subcategories: list[Category] = []
```

