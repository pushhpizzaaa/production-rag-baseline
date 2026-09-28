# Request Example Data and Schema Extras

**Doc ID:** `fastapi_declare_request_example_data`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Enhance OpenAPI interactive docs with realistic JSON examples using json_schema_extra and Field examples.

---

## Declaring Examples in Pydantic v2
Providing realistic request examples dramatically improves developer experience in Swagger UI (`/docs`).

```python
from pydantic import BaseModel, Field
from fastapi import FastAPI

app = FastAPI()

class Item(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "Ergonomic Mechanical Keyboard"})
    description: str | None = Field(None, json_schema_extra={"example": "Custom split keyboard with tactile switches"})
    price: float = Field(..., json_schema_extra={"example": 149.99})

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Noise Cancelling Headphones",
                    "description": "Wireless over-ear headphones with active noise cancelling",
                    "price": 299.00
                }
            ]
        }
    }

@app.post("/items/")
async def create_item(item: Item):
    return item
```

