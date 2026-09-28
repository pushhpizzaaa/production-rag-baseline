# Cookie and Header Parameters

**Doc ID:** `fastapi_cookie_and_header_parameters`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Extract and validate client HTTP cookies and custom headers using Cookie and Header helpers.

---

## Extracting Headers and Cookies
Use `Header` and `Cookie` to declare parameter sources:

```python
from typing import Annotated
from fastapi import FastAPI, Header, Cookie

app = FastAPI()

@app.get("/items/")
async def read_items(
    user_agent: Annotated[str | None, Header(description="Browser User Agent")] = None,
    x_token: Annotated[list[str] | None, Header(description="Custom Auth Tokens")] = None,
    session_id: Annotated[str | None, Cookie()] = None,
):
    return {
        "User-Agent": user_agent,
        "X-Token values": x_token,
        "session_id": session_id
    }
```

### Automatic Underscore to Hyphen Conversion
By default, FastAPI automatically converts underscores in Python parameter names to hyphens in HTTP headers (`user_agent` -> `User-Agent`). To disable this:
```python
x_custom = Header(convert_underscores=False)
```

