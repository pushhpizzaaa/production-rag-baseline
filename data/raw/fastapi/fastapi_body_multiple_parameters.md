# Body - Multiple Parameters and Embeds

**Doc ID:** `fastapi_body_multiple_parameters`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Combine multiple Pydantic body models, singular values, and embedded keys in a single endpoint.

---

## Combining Multiple Body Payloads
FastAPI allows combining multiple Pydantic models in a single request:

```python
from typing import Annotated
from pydantic import BaseModel
from fastapi import FastAPI, Body

app = FastAPI()

class User(BaseModel):
    username: str
    full_name: str | None = None

class Item(BaseModel):
    name: str
    price: float

@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item,
    user: User,
    importance: Annotated[int, Body(gt=0)],
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results
```

Expected JSON body:
```json
{
  "item": {"name": "Laptop", "price": 999.99},
  "user": {"username": "admin", "full_name": "System Admin"},
  "importance": 5
}
```

### Embed Single Model
To force a single Pydantic model under a nested key instead of root:
```python
@app.post("/items/")
async def create_item(item: Annotated[Item, Body(embed=True)]):
    return item
```
JSON body: `{"item": {"name": "Laptop", "price": 999.99}}`.

