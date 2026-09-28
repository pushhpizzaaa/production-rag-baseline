# Dependencies with Yield and Teardown Logic

**Doc ID:** `fastapi_dependencies_with_yield_and_cleanup`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Manage resource lifecycles (database connections, file handles) using yield dependencies.

---

## Managing Lifecycles with Yield
A dependency with `yield` replaces `try...finally` resource managers:

```python
from fastapi import FastAPI, Depends
from typing import Generator

app = FastAPI()

def get_db_session() -> Generator:
    db = {"connected": True}
    try:
        print("Database connection opened")
        yield db
    finally:
        db["connected"] = False
        print("Database connection closed cleanly")

@app.get("/items/")
async def read_items(db: dict = Depends(get_db_session)):
    return {"db_status": db["connected"]}
```
Code before `yield` runs before the path operation. Code after `yield` runs after response generation.

