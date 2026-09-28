# Production Process Management: Gunicorn and Uvicorn Workers

**Doc ID:** `fastapi_production_gunicorn_uvicorn_workers`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Manage worker concurrency and process recycling using Gunicorn with UvicornWorker.

---

## Running Gunicorn with Uvicorn Workers
```bash
gunicorn src.api.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120 \
  --access-logfile -
```
Recommended worker count formula: `(2 * CPU_CORES) + 1`.

