# First Steps with Path Operations

**Doc ID:** `fastapi_first_steps_path_operations`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Path operations define how FastAPI routes HTTP verbs (GET, POST, PUT, DELETE) to specific Python functions.

---

## Understanding Path Operations
In RESTful terminology, a 'path' (also known as endpoint or route) is combined with an HTTP 'operation' (verb) like GET, POST, PUT, DELETE, OPTIONS, HEAD, PATCH, TRACE.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    return {"item_id": item_id, "status": "active"}

@app.post("/items")
async def create_item(payload: dict):
    return {"created": True, "data": payload}
```

### Operation Decorators
- `@app.get()`: Retrieve data.
- `@app.post()`: Create data.
- `@app.put()`: Completely replace existing data.
- `@app.patch()`: Partially update existing data.
- `@app.delete()`: Remove existing data.

### Async vs Sync Path Operations
When you declare a path operation function with `async def`, FastAPI will run it directly in the main event loop. If you declare it with regular `def`, FastAPI runs it in an external threadpool that is then awaited, preventing blocking IO from freezing the server.

