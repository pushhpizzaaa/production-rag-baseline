# Security First Steps: OAuth2 and Bearer Tokens

**Doc ID:** `fastapi_security_first_steps_oauth2`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Understand OAuth2 password flows and Bearer authentication integrated natively in FastAPI.

---

## OAuth2PasswordBearer
FastAPI implements OAuth2 flows using `OAuth2PasswordBearer`:

```python
from typing import Annotated
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
```
In Swagger UI (`/docs`), an 'Authorize' button appears automatically, letting developers input credentials.

