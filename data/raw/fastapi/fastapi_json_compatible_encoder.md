# JSON Compatible Encoder Utility

**Doc ID:** `fastapi_json_compatible_encoder`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Convert arbitrary Python objects (Pydantic models, Datetimes, Sets) into standard JSON-serializable types.

---

## Using jsonable_encoder
FastAPI includes `jsonable_encoder` to convert complex Python objects into JSON-compatible primitives (dicts, lists, strings, numbers):

```python
from datetime import datetime
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

class Order(BaseModel):
    order_id: str
    created_at: datetime
    tags: set[str]

order = Order(order_id="ORD-101", created_at=datetime.utcnow(), tags={"priority", "express"})
json_data = jsonable_encoder(order)

print(type(json_data["created_at"]))  # str: '2026-09-28T16:00:00'
print(type(json_data["tags"]))        # list: ['priority', 'express']
```
Useful before saving entities to databases like MongoDB or Redis that do not accept native Pydantic instances.

