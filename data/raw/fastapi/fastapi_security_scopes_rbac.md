# Security Scopes and Role-Based Access Control (RBAC)

**Doc ID:** `fastapi_security_scopes_rbac`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Implement fine-grained permissions and role checks using SecurityScopes.

---

## Enforcing Scopes
```python
from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer, SecurityScopes

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"me": "Read current user info", "items": "Read items catalogue", "admin": "Full system access"}
)

app = FastAPI()

def verify_permissions(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    token_scopes = ["me", "items"] # extracted from token claims
    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(status_code=403, detail=f"Not enough permissions: requires {scope}")
    return token

@app.get("/admin/metrics", dependencies=[Security(verify_permissions, scopes=["admin"])])
async def get_metrics():
    return {"cpu": "12%"}
```

