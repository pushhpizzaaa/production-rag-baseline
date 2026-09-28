# Dependency Overrides in Automated Test Suites

**Doc ID:** `fastapi_dependency_overrides_in_tests`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Mock external dependencies (databases, auth providers, LLM clients) cleanly during pytest execution.

---

## Mocking with dependency_overrides
```python
from fastapi.testclient import TestClient
from fastapi import FastAPI, Depends

app = FastAPI()

def get_external_service():
    return "real_external_service_call"

@app.get("/service")
def read_service(svc: str = Depends(get_external_service)):
    return {"service": svc}

def test_override():
    app.dependency_overrides[get_external_service] = lambda: "mocked_service"
    client = TestClient(app)
    response = client.get("/service")
    assert response.json() == {"service": "mocked_service"}
    app.dependency_overrides.clear() # Clean up
```

