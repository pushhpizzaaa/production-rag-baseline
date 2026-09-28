# Custom Responses: HTML, PlainText, and Redirects

**Doc ID:** `fastapi_custom_responses_html_plaintext_redirect`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Return non-JSON content types including HTML templates, raw strings, and HTTP redirects.

---

## Specialized Response Classes
```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse

app = FastAPI()

@app.get("/legacy")
async def redirect_old_path():
    return RedirectResponse(url="/new-path", status_code=301)

@app.get("/robot.txt", response_class=PlainTextResponse)
async def robots_txt():
    return "User-agent: *\nDisallow: /admin"

@app.get("/portal", response_class=HTMLResponse)
async def portal_page():
    return "<h1>Developer Portal</h1><p>Documentation available at /docs</p>"
```

