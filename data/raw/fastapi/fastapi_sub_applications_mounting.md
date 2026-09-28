# Sub-Applications and Mount Points

**Doc ID:** `fastapi_sub_applications_mounting`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Mount independent FastAPI or WSGI applications under dedicated path prefixes.

---

## Mounting Sub-Apps
```python
from fastapi import FastAPI

main_app = FastAPI(title="Main API")
admin_app = FastAPI(title="Admin Panel")

@admin_app.get("/dashboard")
def dashboard():
    return {"section": "administration"}

main_app.mount("/admin", admin_app)
```
Each mounted sub-application maintains independent OpenAPI docs (`/admin/docs`).

