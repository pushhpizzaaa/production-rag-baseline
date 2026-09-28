# In-Memory Caching with Redis

**Doc ID:** `fastapi_redis_caching_cachelib`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Cache expensive query results and database lookups in Redis with TTL expiration.

---

## Redis Caching Pattern
```python
import json
import redis
from fastapi import FastAPI

app = FastAPI()
r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

@app.get("/items/{item_id}")
def get_cached_item(item_id: str):
    cache_key = f"item:{item_id}"
    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)
    
    # Compute expensive lookup
    data = {"item_id": item_id, "data": "expensive_result"}
    r.setex(cache_key, 300, json.dumps(data)) # 5 minute TTL
    return data
```

