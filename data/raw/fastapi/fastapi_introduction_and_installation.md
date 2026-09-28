# FastAPI Introduction and Installation

**Doc ID:** `fastapi_introduction_and_installation`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** FastAPI is a modern, high-performance web framework for building APIs with Python 3.8+ based on standard Python type hints.

---

## Installation
Install FastAPI with standard dependencies including uvicorn:
```bash
pip install "fastapi[standard]"
```
FastAPI runs on ASGI (Asynchronous Server Gateway Interface) web servers like Uvicorn or Hypercorn. It relies on Starlette for web tooling and Pydantic for data validation.

## Key Performance Traits
- **Speed**: Very high performance, on par with NodeJS and Go (thanks to Starlette and Pydantic).
- **Fast to code**: Increase the speed to develop features by about 200% to 300%.
- **Fewer bugs**: Reduce about 40% of developer induced (human) errors.
- **Standards-based**: Based on and fully compatible with the open standards for APIs: OpenAPI and JSON Schema.

## Minimal Application
```python
from fastapi import FastAPI

app = FastAPI(title="Production Service")

@app.get("/")
def read_root():
    return {"message": "Service healthy"}
```
Run with:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

