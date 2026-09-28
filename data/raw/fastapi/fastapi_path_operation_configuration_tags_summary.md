# Path Operation Metadata: Tags, Summary, and Description

**Doc ID:** `fastapi_path_operation_configuration_tags_summary`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Organize endpoints in Swagger UI and ReDoc using tags, summary, description, and deprecation flags.

---

## Organizing API Documentation
Add metadata to `@app.get()` decorators to generate clean, professional Swagger documentation:

```python
from fastapi import FastAPI

app = FastAPI()

@app.post(
    "/items/",
    tags=["Inventory Management"],
    summary="Create a new stock item",
    description="Registers a brand new SKU in the warehouse database with initial stock count.",
    response_description="The freshly created item including generated UUID and timestamp.",
    deprecated=False
)
async def create_item(name: str):
    return {"name": name}
```

