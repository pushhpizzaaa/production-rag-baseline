# Response Status Codes and HTTP Semantics

**Doc ID:** `fastapi_response_status_codes`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Set proper HTTP response status codes using the status module to adhere to REST specifications.

---

## Setting HTTP Status Codes
HTTP status codes convey execution results to clients:

```python
from fastapi import FastAPI, status, HTTPException

app = FastAPI()

@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name, "status": "created"}

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    # Returns empty body with HTTP 204
    return None
```

### Common Status Codes
- `200 OK`: Standard successful response.
- `201 CREATED`: Resource created successfully.
- `202 ACCEPTED`: Asynchronous job queued.
- `204 NO CONTENT`: Action succeeded, no body returned.
- `400 BAD REQUEST`: Invalid client input.
- `401 UNAUTHORIZED`: Authentication credentials missing or invalid.
- `403 FORBIDDEN`: Valid identity, but lacks required role/permission.
- `404 NOT FOUND`: Target entity does not exist.
- `422 UNPROCESSABLE ENTITY`: Schema validation failed.

