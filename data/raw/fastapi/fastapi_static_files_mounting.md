# Static Files Mounting and CDN Serving

**Doc ID:** `fastapi_static_files_mounting`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Serve static web assets (CSS, JavaScript, images) using Starlette StaticFiles.

---

## Mounting Static Assets
```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

static_dir = Path("static")
static_dir.mkdir(exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
```
Files inside `./static` are served under `http://localhost:8000/static/filename.ext`.

