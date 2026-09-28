# Testing APIs with Pytest and TestClient

**Doc ID:** `fastapi_testing_with_pytest_and_testclient`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Write automated unit and integration tests using Starlette TestClient (powered by httpx).

---

## Testing with TestClient
```python
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

app = FastAPI()

@app.get("/ping")
def ping():
    return {"status": "pong"}

client = TestClient(app)

def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"status": "pong"}
```
TestClient runs synchronously without starting a real network socket, making tests fast and deterministic.

