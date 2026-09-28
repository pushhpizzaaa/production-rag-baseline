# Handling Errors with HTTPException

**Doc ID:** `fastapi_handling_errors_http_exception`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Raise HTTPException to abort processing and return clear error status codes and messages to API consumers.

---

## Using HTTPException
When validation or business logic fails, raise `HTTPException`:

```python
from fastapi import FastAPI, HTTPException, status

app = FastAPI()

fake_db = {"item_1": "Mechanical Keyboard"}

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in fake_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item '{item_id}' not found in database",
            headers={"X-Error-Reason": "EntityNotFound"}
        )
    return {"item": fake_db[item_id]}
```

### Custom Error Headers
The optional `headers` dictionary allows attaching diagnostic or security headers (such as `WWW-Authenticate: Bearer` for 401 Unauthorized responses).

