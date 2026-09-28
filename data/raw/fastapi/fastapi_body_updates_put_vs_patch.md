# Body Updates: PUT vs PATCH Implementations

**Doc ID:** `fastapi_body_updates_put_vs_patch`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Implement full replacement (PUT) and partial updates (PATCH) using model_dump(exclude_unset=True).

---

## Implementing PUT vs PATCH
- **PUT**: Replaces the entire resource. Missing fields are reset to default or null.
- **PATCH**: Updates only fields provided by the caller.

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    description: str | None = None

class ItemPatch(BaseModel):
    name: str | None = None
    price: float | None = None
    description: str | None = None

items_db = {"item_1": {"name": "Monitor", "price": 250.0, "description": "4K IPS"}}

@app.patch("/items/{item_id}", response_model=Item)
async def patch_item(item_id: str, patch_data: ItemPatch):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    stored_item = items_db[item_id]
    # Key technique: exclude_unset=True ignores fields not provided in request
    update_data = patch_data.model_dump(exclude_unset=True)
    stored_item.update(update_data)
    items_db[item_id] = stored_item
    return stored_item
```

