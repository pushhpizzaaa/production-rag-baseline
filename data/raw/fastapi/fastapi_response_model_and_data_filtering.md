# Response Model and Data Filtering

**Doc ID:** `fastapi_response_model_and_data_filtering`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Control output serialization and filter out sensitive data like passwords using response_model.

---

## Security and Data Filtering with response_model
Never return raw database entities containing sensitive fields (like password hashes). Define a dedicated output schema:

```python
from pydantic import BaseModel, EmailStr
from fastapi import FastAPI

app = FastAPI()

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr

class UserOut(BaseModel):
    username: str
    email: EmailStr

@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn):
    # password is safe in user.password, but excluded from HTTP response
    return user
```

### Filtering Defaults and None
- `response_model_exclude_unset=True`: Only include fields explicitly set by application.
- `response_model_exclude_none=True`: Omit keys with None value.
- `response_model_include={"username", "email"}`: Whitelist specific fields.

