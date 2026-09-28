# Form Data and URL-Encoded Requests

**Doc ID:** `fastapi_form_data_and_fields`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Process HTML form submissions encoded as application/x-www-form-urlencoded using the Form class.

---

## Receiving Form Data
Form data is sent as URL-encoded key-values instead of JSON:

```bash
pip install python-multipart
```

```python
from typing import Annotated
from fastapi import FastAPI, Form

app = FastAPI()

@app.post("/login/")
async def login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
):
    return {"username": username, "auth_type": "form_urlencoded"}
```

### Difference from JSON Body
When using `Form()`, FastAPI parses `application/x-www-form-urlencoded`. You cannot simultaneously declare a raw JSON body in the same request because HTTP permits only one `Content-Type` header per request.

