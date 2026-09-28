# Dependencies in Path Operation Decorators

**Doc ID:** `fastapi_dependencies_in_path_operation_decorators`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Enforce execution of dependencies at the path level without passing their return values into function arguments.

---

## Router and Decorator Dependencies
When you want to enforce validation (like API key verification) but do not need its return value inside the handler:

```python
from fastapi import FastAPI, Depends, HTTPException, Header

app = FastAPI()

async def verify_admin_header(x_admin_secret: str = Header(...)):
    if x_admin_secret != "super-admin-vault":
        raise HTTPException(status_code=403, detail="Forbidden")

@app.post("/admin/reset-database", dependencies=[Depends(verify_admin_header)])
async def reset_database():
    return {"status": "Database cleared"}
```

