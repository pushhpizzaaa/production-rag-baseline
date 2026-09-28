# Extra Models: Union, Polymorphism and Inheritance

**Doc ID:** `fastapi_extra_models_union_polymorphism`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Support polymorphic response and request schemas using Python Union types and discriminated unions.

---

## Polymorphic Payloads with Union
When an endpoint can return multiple schemas, declare a `Union`:

```python
from typing import Union, Literal
from pydantic import BaseModel, Field
from fastapi import FastAPI

app = FastAPI()

class Car(BaseModel):
    vehicle_type: Literal["car"] = "car"
    doors: int

class Motorcycle(BaseModel):
    vehicle_type: Literal["motorcycle"] = "motorcycle"
    has_sidecar: bool

Vehicle = Union[Car, Motorcycle]

@app.get("/vehicles/{vehicle_id}", response_model=Vehicle)
async def get_vehicle(vehicle_id: str):
    if vehicle_id == "c1":
        return Car(doors=4)
    return Motorcycle(has_sidecar=False)
```

### Discriminated Unions in OpenAPI
Using `Literal` as a discriminator field (`vehicle_type`) ensures OpenAPI generates clean `anyOf` / `oneOf` schemas in client SDKs.

