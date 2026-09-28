# Global Dependencies for Applications and Routers

**Doc ID:** `fastapi_global_dependencies`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Apply security or telemetry dependencies globally across every route in an application or router.

---

## Global Application Dependencies
Pass `dependencies` during `FastAPI()` instantiation to enforce rules globally:

```python
from fastapi import FastAPI, Depends, Header, HTTPException

async def verify_api_version(x_api_version: str = Header(default="v1")):
    if x_api_version not in ["v1", "v2"]:
        raise HTTPException(status_code=400, detail="Unsupported API Version")

app = FastAPI(dependencies=[Depends(verify_api_version)])

@app.get("/users/")
async def get_users():
    return [{"user": "alice"}]
```

