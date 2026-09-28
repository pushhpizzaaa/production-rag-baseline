# Asynchronous Task Queues with Celery

**Doc ID:** `fastapi_celery_task_queue_integration`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Offload heavy distributed computational jobs and background workers using Celery and Redis.

---

## Offloading to Celery
```python
from fastapi import FastAPI
from celery import Celery

celery_app = Celery("tasks", broker="redis://localhost:6379/0", backend="redis://localhost:6379/1")

@celery_app.task
def heavy_nlp_extraction(document_id: str):
    return {"document_id": document_id, "status": "extracted"}

app = FastAPI()

@app.post("/extract-job/{doc_id}")
async def schedule_job(doc_id: str):
    task = heavy_nlp_extraction.delay(doc_id)
    return {"task_id": task.id, "state": "PENDING"}
```

