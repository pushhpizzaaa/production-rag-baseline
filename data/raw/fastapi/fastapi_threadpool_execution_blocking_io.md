# Threadpool Execution and Concurrency Limits

**Doc ID:** `fastapi_threadpool_execution_blocking_io`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Configure AnyIO worker threadpool limits to optimize blocking library throughput.

---

## Configuring Threadpool Capacity
FastAPI relies on AnyIO / Starlette worker threads for regular `def` routes:
```python
import anyio
from fastapi import FastAPI

app = FastAPI()

@app.on_event("startup")
async def configure_concurrency():
    limiter = anyio.to_thread.current_default_thread_limiter()
    limiter.total_tokens = 100 # increase default threadpool cap from 40 to 100
```

