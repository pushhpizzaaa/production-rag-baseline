# Extra Data Types: UUIDs, Dates, and Timedeltas

**Doc ID:** `fastapi_extra_data_types_uuids_dates`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** FastAPI supports native parsing and validation for UUID, datetime, date, and timedelta objects.

---

## Supported Extra Data Types
FastAPI seamlessly parses and validates complex standard library types:

```python
from datetime import datetime, time, timedelta
from uuid import UUID
from typing import Annotated
from fastapi import FastAPI, Body

app = FastAPI()

@app.put("/items/{item_id}")
async def update_item(
    item_id: UUID,
    start_datetime: Annotated[datetime | None, Body()] = None,
    end_datetime: Annotated[datetime | None, Body()] = None,
    process_after: Annotated[timedelta | None, Body()] = None,
):
    duration = end_datetime - start_datetime if end_datetime and start_datetime else None
    return {
        "item_id": item_id,
        "start": start_datetime,
        "duration_seconds": duration.total_seconds() if duration else 0
    }
```

### Key Formats
- `UUID`: Validates RFC 4122 format like `3fa85f64-5717-4562-b3fc-2c963f66afa6`.
- `datetime`: ISO 8601 string like `2026-09-28T12:00:00Z`.
- `timedelta`: Number of seconds or ISO 8601 duration (e.g. `PT2H`).

