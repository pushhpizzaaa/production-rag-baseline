# Request Files and UploadFile Handling

**Doc ID:** `fastapi_request_files_and_uploadfile`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Handle binary file uploads efficiently using UploadFile with streaming spooling for large files.

---

## UploadFile vs bytes
FastAPI provides `UploadFile` which wraps a SpooledTemporaryFile:

```python
from fastapi import FastAPI, UploadFile, File, HTTPException
import shutil
from pathlib import Path

app = FastAPI()
UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Validate extension or mime
    if not file.filename.endswith((".pdf", ".png", ".jpg")):
        raise HTTPException(status_code=400, detail="Invalid file type")

    destination = UPLOAD_DIR / file.filename
    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size_bytes": destination.stat().st_size
    }
```

### Advantages of UploadFile
- Files larger than memory threshold (default 1MB) are written to disk, preventing Out-Of-Memory crashes.
- Exposes async methods: `await file.read()`, `await file.seek()`, `await file.close()`.

