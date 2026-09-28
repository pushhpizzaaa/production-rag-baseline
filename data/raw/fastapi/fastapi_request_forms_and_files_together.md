# Combining Form Fields and File Uploads

**Doc ID:** `fastapi_request_forms_and_files_together`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Accept metadata forms and binary file attachments simultaneously in multipart/form-data requests.

---

## Handling Multipart Forms with Files
Clients frequently upload files alongside contextual metadata:

```python
from typing import Annotated
from fastapi import FastAPI, File, Form, UploadFile

app = FastAPI()

@app.post("/documents/")
async def create_document(
    title: Annotated[str, Form(min_length=3)],
    description: Annotated[str | None, Form()] = None,
    file: UploadFile = File(...),
):
    contents = await file.read()
    return {
        "title": title,
        "description": description,
        "filename": file.filename,
        "bytes_received": len(contents)
    }
```

