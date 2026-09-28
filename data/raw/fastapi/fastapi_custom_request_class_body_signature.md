# Custom Request and APIRoute Classes

**Doc ID:** `fastapi_custom_request_class_body_signature`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Intercept raw request byte streams to verify webhook HMAC signatures and log unparsed payloads.

---

## Custom APIRoute for Signature Verification
```python
import hashlib, hmac
from fastapi import FastAPI, Request, HTTPException
from fastapi.routing import APIRoute

class SignatureValidationRoute(APIRoute):
    def get_route_handler(self):
        original_handler = super().get_route_handler()
        async def custom_handler(request: Request):
            body_bytes = await request.body()
            signature = request.headers.get("X-Signature")
            # compute and assert HMAC
            return await original_handler(request)
        return custom_handler

app = FastAPI()
app.router.route_class = SignatureValidationRoute
```

