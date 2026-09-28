# Server-Sent Events (SSE) for Real-Time LLM Token Streaming

**Doc ID:** `fastapi_server_sent_events_sse`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Stream real-time events over standard HTTP connections using the text/event-stream format.

---

## Server-Sent Events Protocol
SSE transmits text formatted as `data: <content>\n\n`:

```python
import asyncio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

async def event_generator():
    for i in range(5):
        yield f"event: update\ndata: {{"step": {i}}}\n\n"
        await asyncio.sleep(0.1)

@app.get("/events")
async def events():
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
    )
```

