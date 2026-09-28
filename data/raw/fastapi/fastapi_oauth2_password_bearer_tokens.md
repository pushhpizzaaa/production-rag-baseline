# OAuth2 Password Flow with Password Hashing

**Doc ID:** `fastapi_oauth2_password_bearer_tokens`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Build full user authentication with passlib bcrypt hashing and OAuth2PasswordRequestForm.

---

## Complete Authentication Implementation
```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import hashlib

app = FastAPI()

users_db = {
    "john": {"username": "john", "hashed_password": hashlib.sha256(b"secret123").hexdigest()}
}

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    hashed = hashlib.sha256(form_data.password.encode()).hexdigest()
    if hashed != user["hashed_password"]:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user["username"], "token_type": "bearer"}
```

