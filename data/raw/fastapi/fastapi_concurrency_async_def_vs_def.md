# Concurrency Deep Dive: async def vs def Path Handlers

**Doc ID:** `fastapi_concurrency_async_def_vs_def`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Understand threadpools, event loops, and CPU-bound vs IO-bound performance in FastAPI.

---

## The Critical Difference
- **`async def`**: Runs directly inside the main asyncio event loop.
  - MUST NOT call blocking synchronous IO (e.g. `time.sleep()`, standard `requests.get()`, synchronous SQLite/psycopg2).
  - Use when awaiting non-blocking IO (`httpx.AsyncClient`, `aiofiles`, asyncpg).
- **`def` (regular function)**: FastAPI automatically schedules this function onto a separate worker thread (`anyio.to_thread.run_sync`).
  - Safe for legacy blocking synchronous libraries.
  - Slower than pure async due to thread context-switching overhead.

```python
import time
import asyncio
from fastapi import FastAPI

app = FastAPI()

@app.get("/sync-blocking")
def sync_blocking():
    time.sleep(1) # OK: runs in external threadpool
    return {"worker": "threadpool"}

@app.get("/async-nonblocking")
async def async_nonblocking():
    await asyncio.sleep(1) # OK: cooperative async sleep
    return {"worker": "event_loop"}
```

