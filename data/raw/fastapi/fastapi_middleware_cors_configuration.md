# CORS Middleware Configuration

**Doc ID:** `fastapi_middleware_cors_configuration`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Enable Cross-Origin Resource Sharing (CORS) to allow browser web apps to consume APIs securely.

---

## Configuring CORSMiddleware
Browsers block cross-origin HTTP requests by default. Configure `CORSMiddleware`:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://myproductionapp.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
    max_age=86400,
)
```
Avoid using `allow_origins=["*"]` when `allow_credentials=True` in production systems.

