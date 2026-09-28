# Path Parameters and Type Validation

**Doc ID:** `fastapi_path_parameters_and_types`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Declare path parameters with Python type hints to get automatic parsing, validation, and OpenAPI documentation.

---

## Declaring Path Parameters
Path parameters are embedded inside URL path segments using curly braces `{}`:

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/users/{user_id}")
async def read_user(user_id: int):
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="User ID must be positive")
    return {"user_id": user_id}
```

### Automatic Type Conversion and Validation
If a client sends `/users/foo`, FastAPI automatically returns a structured HTTP 422 Unprocessable Entity response:
```json
{
  "detail": [
    {
      "loc": ["path", "user_id"],
      "msg": "Input should be a valid integer, unable to parse string as an integer",
      "type": "int_parsing"
    }
  ]
}
```

### Predefined Values with Enums
To restrict a path parameter to a fixed set of choices, use Python's `enum.Enum`:
```python
from enum import Enum
from fastapi import FastAPI

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    return {"model_name": model_name, "message": "Have some residuals"}
```

