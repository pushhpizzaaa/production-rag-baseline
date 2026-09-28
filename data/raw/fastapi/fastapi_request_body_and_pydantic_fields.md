# Request Body and Pydantic Fields

**Doc ID:** `fastapi_request_body_and_pydantic_fields`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Define complex JSON request bodies using Pydantic BaseModel with rich Field constraints and defaults.

---

## Pydantic BaseModel in FastAPI
When receiving data from clients in HTTP POST/PUT requests, declare the schema as a Pydantic model:

```python
from typing import Annotated
from pydantic import BaseModel, Field
from fastapi import FastAPI

app = FastAPI()

class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Item name")
    description: str | None = Field(default=None, max_length=300)
    price: float = Field(..., gt=0.0, description="Price must be greater than zero")
    tax: float | None = Field(default=None, ge=0.0)
    tags: set[str] = Field(default_factory=set)

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax:
        total_price = item.price + item.tax
        item_dict.update({"total_price": total_price})
    return item_dict
```

### Field Metadata Attributes
- `...` (Ellipsis) or omitting default indicates required field.
- `title`, `description`: Shown in OpenAPI documentation.
- `examples`: List of illustrative JSON values for interactive documentation.

