# Streaming Responses and Large File Downloads

**Doc ID:** `fastapi_streaming_responses_and_iterators`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Stream LLM tokens and continuous binary data chunks using StreamingResponse.

---

## Streaming Data Chunks
```python
import asyncio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

async def fake_token_stream():
    for word in ["Retrieval-Augmented ", "Generation ", "delivers ", "grounded ", "answers."]:
        yield word.encode("utf-8")
        await asyncio.sleep(0.05)

@app.get("/stream-answer")
async def stream_answer():
    return StreamingResponse(fake_token_stream(), media_type="text/plain")
```
Crucial for LLM token streaming (Server-Sent Events) and multi-gigabyte file transfers without memory exhaustion.

