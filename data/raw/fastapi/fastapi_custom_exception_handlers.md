# Custom Exception Handlers and Global Interception

**Doc ID:** `fastapi_custom_exception_handlers`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Register application-wide exception handlers for domain exceptions and override validation error formats.

---

## Registering Custom Exception Handlers
Intercept custom domain exceptions and format responses consistently across your API:

```python
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

class ItemNotFoundError(Exception):
    def __init__(self, item_id: str):
        self.item_id = item_id

app = FastAPI()

@app.exception_handler(ItemNotFoundError)
async def item_not_found_handler(request: Request, exc: ItemNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error_code": "RESOURCE_MISSING",
            "message": f"Resource with ID {exc.item_id} does not exist",
            "path": str(request.url.path),
        }
    )
```

### Overriding RequestValidationError
To customize FastAPI's default 422 error body:
```python
from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"validation_errors": exc.errors(), "body": exc.body}
    )
```

