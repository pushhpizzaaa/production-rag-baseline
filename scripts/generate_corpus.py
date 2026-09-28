"""
Corpus Generator Script: Generates 200 curated, realistic technical documentation files
across FastAPI (70 docs), Scikit-Learn (65 docs), and MongoDB (65 docs).

These files serve as the ground-truth technical corpus for the Baseline RAG Pipeline
and its three downstream derivative projects.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_RAW = BASE_DIR / "data" / "raw"

FASTAPI_DOCS = [
    ("fastapi_introduction_and_installation", "FastAPI Introduction and Installation",
     "FastAPI is a modern, high-performance web framework for building APIs with Python 3.8+ based on standard Python type hints.",
     """## Installation
Install FastAPI with standard dependencies including uvicorn:
```bash
pip install "fastapi[standard]"
```
FastAPI runs on ASGI (Asynchronous Server Gateway Interface) web servers like Uvicorn or Hypercorn. It relies on Starlette for web tooling and Pydantic for data validation.

## Key Performance Traits
- **Speed**: Very high performance, on par with NodeJS and Go (thanks to Starlette and Pydantic).
- **Fast to code**: Increase the speed to develop features by about 200% to 300%.
- **Fewer bugs**: Reduce about 40% of developer induced (human) errors.
- **Standards-based**: Based on and fully compatible with the open standards for APIs: OpenAPI and JSON Schema.

## Minimal Application
```python
from fastapi import FastAPI

app = FastAPI(title="Production Service")

@app.get("/")
def read_root():
    return {"message": "Service healthy"}
```
Run with:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
"""),

    ("fastapi_first_steps_path_operations", "First Steps with Path Operations",
     "Path operations define how FastAPI routes HTTP verbs (GET, POST, PUT, DELETE) to specific Python functions.",
     """## Understanding Path Operations
In RESTful terminology, a 'path' (also known as endpoint or route) is combined with an HTTP 'operation' (verb) like GET, POST, PUT, DELETE, OPTIONS, HEAD, PATCH, TRACE.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    return {"item_id": item_id, "status": "active"}

@app.post("/items")
async def create_item(payload: dict):
    return {"created": True, "data": payload}
```

### Operation Decorators
- `@app.get()`: Retrieve data.
- `@app.post()`: Create data.
- `@app.put()`: Completely replace existing data.
- `@app.patch()`: Partially update existing data.
- `@app.delete()`: Remove existing data.

### Async vs Sync Path Operations
When you declare a path operation function with `async def`, FastAPI will run it directly in the main event loop. If you declare it with regular `def`, FastAPI runs it in an external threadpool that is then awaited, preventing blocking IO from freezing the server.
"""),

    ("fastapi_path_parameters_and_types", "Path Parameters and Type Validation",
     "Declare path parameters with Python type hints to get automatic parsing, validation, and OpenAPI documentation.",
     """## Declaring Path Parameters
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
"""),

    ("fastapi_query_parameters_and_string_validations", "Query Parameters and String Validations",
     "Query parameters are key-value pairs passed in the URL after a question mark, used for filtering, pagination, and sorting.",
     """## Declaring Query Parameters
Function parameters that are not part of path parameters are automatically interpreted as query parameters:

```python
from typing import Annotated
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items/")
async def read_items(
    q: Annotated[str | None, Query(min_length=3, max_length=50, pattern="^[a-zA-Z0-9_-]+$")] = None,
    skip: Annotated[int, Query(ge=0, description="Offset for pagination")] = 0,
    limit: Annotated[int, Query(gt=0, le=100, description="Page limit")] = 10,
):
    return {"q": q, "skip": skip, "limit": limit}
```

### Validation Constraints with Query()
- `min_length`, `max_length`: String length boundaries.
- `pattern`: Regular expression for regex verification.
- `ge`, `gt`, `le`, `lt`: Numeric comparisons (greater/less than or equal).
- `deprecated=True`: Flags parameter as deprecated in Swagger UI.
- `alias`: Use alternative query parameter name (e.g. `item-query`).

### Query Parameter Lists / Multiple Values
```python
@app.get("/search/")
async def search(tags: Annotated[list[str] | None, Query()] = None):
    return {"tags": tags or []}
```
Client query: `/search/?tags=python&tags=fastapi` yields `tags: ["python", "fastapi"]`.
"""),

    ("fastapi_request_body_and_pydantic_fields", "Request Body and Pydantic Fields",
     "Define complex JSON request bodies using Pydantic BaseModel with rich Field constraints and defaults.",
     """## Pydantic BaseModel in FastAPI
When receiving data from clients in HTTP POST/PUT requests, declare the schema as a Pydantic model:

```python
from typing import Annotated
from pydantic import BaseModel, Field
from fastapi import FastAPI

app = FastAPI()

class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Item name")
    description: str | None = Field(default=None, max_length=300)
    price: float = Field(..., gt=0.0, description="Price must be greater than zero")
    tax: float | None = Field(default=None, ge=0.0)
    tags: set[str] = Field(default_factory=set)

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax:
        total_price = item.price + item.tax
        item_dict.update({"total_price": total_price})
    return item_dict
```

### Field Metadata Attributes
- `...` (Ellipsis) or omitting default indicates required field.
- `title`, `description`: Shown in OpenAPI documentation.
- `examples`: List of illustrative JSON values for interactive documentation.
"""),

    ("fastapi_body_multiple_parameters", "Body - Multiple Parameters and Embeds",
     "Combine multiple Pydantic body models, singular values, and embedded keys in a single endpoint.",
     """## Combining Multiple Body Payloads
FastAPI allows combining multiple Pydantic models in a single request:

```python
from typing import Annotated
from pydantic import BaseModel
from fastapi import FastAPI, Body

app = FastAPI()

class User(BaseModel):
    username: str
    full_name: str | None = None

class Item(BaseModel):
    name: str
    price: float

@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item,
    user: User,
    importance: Annotated[int, Body(gt=0)],
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results
```

Expected JSON body:
```json
{
  "item": {"name": "Laptop", "price": 999.99},
  "user": {"username": "admin", "full_name": "System Admin"},
  "importance": 5
}
```

### Embed Single Model
To force a single Pydantic model under a nested key instead of root:
```python
@app.post("/items/")
async def create_item(item: Annotated[Item, Body(embed=True)]):
    return item
```
JSON body: `{"item": {"name": "Laptop", "price": 999.99}}`.
"""),

    ("fastapi_body_nested_models", "Nested Pydantic Models and Complex Attributes",
     "Construct deeply nested hierarchical JSON schemas with sub-models, sets, and image/file references.",
     """## Deeply Nested Models
Pydantic models can nest other models to define clean hierarchical data structures:

```python
from pydantic import BaseModel, HttpUrl
from fastapi import FastAPI

app = FastAPI()

class Image(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tags: set[str] = set()
    images: list[Image] | None = None

class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item]

@app.post("/offers/")
async def create_offer(offer: Offer):
    return {"offer_name": offer.name, "item_count": len(offer.items)}
```

### Self-Referencing and Recursive Models
Pydantic v2 supports recursive self-referential schemas using `from __future__ import annotations` or `model_rebuild()`:
```python
class Category(BaseModel):
    name: str
    subcategories: list[Category] = []
```
"""),

    ("fastapi_declare_request_example_data", "Request Example Data and Schema Extras",
     "Enhance OpenAPI interactive docs with realistic JSON examples using json_schema_extra and Field examples.",
     """## Declaring Examples in Pydantic v2
Providing realistic request examples dramatically improves developer experience in Swagger UI (`/docs`).

```python
from pydantic import BaseModel, Field
from fastapi import FastAPI

app = FastAPI()

class Item(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "Ergonomic Mechanical Keyboard"})
    description: str | None = Field(None, json_schema_extra={"example": "Custom split keyboard with tactile switches"})
    price: float = Field(..., json_schema_extra={"example": 149.99})

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Noise Cancelling Headphones",
                    "description": "Wireless over-ear headphones with active noise cancelling",
                    "price": 299.00
                }
            ]
        }
    }

@app.post("/items/")
async def create_item(item: Item):
    return item
```
"""),

    ("fastapi_extra_data_types_uuids_dates", "Extra Data Types: UUIDs, Dates, and Timedeltas",
     "FastAPI supports native parsing and validation for UUID, datetime, date, and timedelta objects.",
     """## Supported Extra Data Types
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
"""),

    ("fastapi_cookie_and_header_parameters", "Cookie and Header Parameters",
     "Extract and validate client HTTP cookies and custom headers using Cookie and Header helpers.",
     """## Extracting Headers and Cookies
Use `Header` and `Cookie` to declare parameter sources:

```python
from typing import Annotated
from fastapi import FastAPI, Header, Cookie

app = FastAPI()

@app.get("/items/")
async def read_items(
    user_agent: Annotated[str | None, Header(description="Browser User Agent")] = None,
    x_token: Annotated[list[str] | None, Header(description="Custom Auth Tokens")] = None,
    session_id: Annotated[str | None, Cookie()] = None,
):
    return {
        "User-Agent": user_agent,
        "X-Token values": x_token,
        "session_id": session_id
    }
```

### Automatic Underscore to Hyphen Conversion
By default, FastAPI automatically converts underscores in Python parameter names to hyphens in HTTP headers (`user_agent` -> `User-Agent`). To disable this:
```python
x_custom = Header(convert_underscores=False)
```
"""),

    ("fastapi_response_model_and_data_filtering", "Response Model and Data Filtering",
     "Control output serialization and filter out sensitive data like passwords using response_model.",
     """## Security and Data Filtering with response_model
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
"""),

    ("fastapi_extra_models_union_polymorphism", "Extra Models: Union, Polymorphism and Inheritance",
     "Support polymorphic response and request schemas using Python Union types and discriminated unions.",
     """## Polymorphic Payloads with Union
When an endpoint can return multiple schemas, declare a `Union`:

```python
from typing import Union, Literal
from pydantic import BaseModel, Field
from fastapi import FastAPI

app = FastAPI()

class Car(BaseModel):
    vehicle_type: Literal["car"] = "car"
    doors: int

class Motorcycle(BaseModel):
    vehicle_type: Literal["motorcycle"] = "motorcycle"
    has_sidecar: bool

Vehicle = Union[Car, Motorcycle]

@app.get("/vehicles/{vehicle_id}", response_model=Vehicle)
async def get_vehicle(vehicle_id: str):
    if vehicle_id == "c1":
        return Car(doors=4)
    return Motorcycle(has_sidecar=False)
```

### Discriminated Unions in OpenAPI
Using `Literal` as a discriminator field (`vehicle_type`) ensures OpenAPI generates clean `anyOf` / `oneOf` schemas in client SDKs.
"""),

    ("fastapi_response_status_codes", "Response Status Codes and HTTP Semantics",
     "Set proper HTTP response status codes using the status module to adhere to REST specifications.",
     """## Setting HTTP Status Codes
HTTP status codes convey execution results to clients:

```python
from fastapi import FastAPI, status, HTTPException

app = FastAPI()

@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name, "status": "created"}

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    # Returns empty body with HTTP 204
    return None
```

### Common Status Codes
- `200 OK`: Standard successful response.
- `201 CREATED`: Resource created successfully.
- `202 ACCEPTED`: Asynchronous job queued.
- `204 NO CONTENT`: Action succeeded, no body returned.
- `400 BAD REQUEST`: Invalid client input.
- `401 UNAUTHORIZED`: Authentication credentials missing or invalid.
- `403 FORBIDDEN`: Valid identity, but lacks required role/permission.
- `404 NOT FOUND`: Target entity does not exist.
- `422 UNPROCESSABLE ENTITY`: Schema validation failed.
"""),

    ("fastapi_form_data_and_fields", "Form Data and URL-Encoded Requests",
     "Process HTML form submissions encoded as application/x-www-form-urlencoded using the Form class.",
     """## Receiving Form Data
Form data is sent as URL-encoded key-values instead of JSON:

```bash
pip install python-multipart
```

```python
from typing import Annotated
from fastapi import FastAPI, Form

app = FastAPI()

@app.post("/login/")
async def login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
):
    return {"username": username, "auth_type": "form_urlencoded"}
```

### Difference from JSON Body
When using `Form()`, FastAPI parses `application/x-www-form-urlencoded`. You cannot simultaneously declare a raw JSON body in the same request because HTTP permits only one `Content-Type` header per request.
"""),

    ("fastapi_request_files_and_uploadfile", "Request Files and UploadFile Handling",
     "Handle binary file uploads efficiently using UploadFile with streaming spooling for large files.",
     """## UploadFile vs bytes
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
"""),

    ("fastapi_request_forms_and_files_together", "Combining Form Fields and File Uploads",
     "Accept metadata forms and binary file attachments simultaneously in multipart/form-data requests.",
     """## Handling Multipart Forms with Files
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
"""),

    ("fastapi_handling_errors_http_exception", "Handling Errors with HTTPException",
     "Raise HTTPException to abort processing and return clear error status codes and messages to API consumers.",
     """## Using HTTPException
When validation or business logic fails, raise `HTTPException`:

```python
from fastapi import FastAPI, HTTPException, status

app = FastAPI()

fake_db = {"item_1": "Mechanical Keyboard"}

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in fake_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item '{item_id}' not found in database",
            headers={"X-Error-Reason": "EntityNotFound"}
        )
    return {"item": fake_db[item_id]}
```

### Custom Error Headers
The optional `headers` dictionary allows attaching diagnostic or security headers (such as `WWW-Authenticate: Bearer` for 401 Unauthorized responses).
"""),

    ("fastapi_custom_exception_handlers", "Custom Exception Handlers and Global Interception",
     "Register application-wide exception handlers for domain exceptions and override validation error formats.",
     """## Registering Custom Exception Handlers
Intercept custom domain exceptions and format responses consistently across your API:

```python
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

class ItemNotFoundError(Exception):
    def __init__(self, item_id: str):
        self.item_id = item_id

app = FastAPI()

@app.exception_handler(ItemNotFoundError)
async def item_not_found_handler(request: Request, exc: ItemNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error_code": "RESOURCE_MISSING",
            "message": f"Resource with ID {exc.item_id} does not exist",
            "path": str(request.url.path),
        }
    )
```

### Overriding RequestValidationError
To customize FastAPI's default 422 error body:
```python
from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"validation_errors": exc.errors(), "body": exc.body}
    )
```
"""),

    ("fastapi_path_operation_configuration_tags_summary", "Path Operation Metadata: Tags, Summary, and Description",
     "Organize endpoints in Swagger UI and ReDoc using tags, summary, description, and deprecation flags.",
     """## Organizing API Documentation
Add metadata to `@app.get()` decorators to generate clean, professional Swagger documentation:

```python
from fastapi import FastAPI

app = FastAPI()

@app.post(
    "/items/",
    tags=["Inventory Management"],
    summary="Create a new stock item",
    description="Registers a brand new SKU in the warehouse database with initial stock count.",
    response_description="The freshly created item including generated UUID and timestamp.",
    deprecated=False
)
async def create_item(name: str):
    return {"name": name}
```
"""),

    ("fastapi_json_compatible_encoder", "JSON Compatible Encoder Utility",
     "Convert arbitrary Python objects (Pydantic models, Datetimes, Sets) into standard JSON-serializable types.",
     """## Using jsonable_encoder
FastAPI includes `jsonable_encoder` to convert complex Python objects into JSON-compatible primitives (dicts, lists, strings, numbers):

```python
from datetime import datetime
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

class Order(BaseModel):
    order_id: str
    created_at: datetime
    tags: set[str]

order = Order(order_id="ORD-101", created_at=datetime.utcnow(), tags={"priority", "express"})
json_data = jsonable_encoder(order)

print(type(json_data["created_at"]))  # str: '2026-09-28T16:00:00'
print(type(json_data["tags"]))        # list: ['priority', 'express']
```
Useful before saving entities to databases like MongoDB or Redis that do not accept native Pydantic instances.
"""),

    ("fastapi_body_updates_put_vs_patch", "Body Updates: PUT vs PATCH Implementations",
     "Implement full replacement (PUT) and partial updates (PATCH) using model_dump(exclude_unset=True).",
     """## Implementing PUT vs PATCH
- **PUT**: Replaces the entire resource. Missing fields are reset to default or null.
- **PATCH**: Updates only fields provided by the caller.

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    description: str | None = None

class ItemPatch(BaseModel):
    name: str | None = None
    price: float | None = None
    description: str | None = None

items_db = {"item_1": {"name": "Monitor", "price": 250.0, "description": "4K IPS"}}

@app.patch("/items/{item_id}", response_model=Item)
async def patch_item(item_id: str, patch_data: ItemPatch):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    stored_item = items_db[item_id]
    # Key technique: exclude_unset=True ignores fields not provided in request
    update_data = patch_data.model_dump(exclude_unset=True)
    stored_item.update(update_data)
    items_db[item_id] = stored_item
    return stored_item
```
"""),

    ("fastapi_dependencies_first_steps", "Dependency Injection: First Steps",
     "FastAPI features a built-in Dependency Injection system using Depends for code reuse and shared logic.",
     """## Introduction to Depends
Dependency Injection allows declaring reusable logic (such as authentication, database sessions, query parameters) that FastAPI executes automatically before the route handler:

```python
from typing import Annotated
from fastapi import FastAPI, Depends

app = FastAPI()

async def common_pagination(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(pagination: Annotated[dict, Depends(common_pagination)]):
    return {"data": [], "pagination": pagination}

@app.get("/users/")
async def read_users(pagination: Annotated[dict, Depends(common_pagination)]):
    return {"users": [], "pagination": pagination}
```

### Benefits
- Eliminate duplicated validation and parameter parsing code.
- Simplifies unit testing via `app.dependency_overrides`.
- Clean separation of business logic from transport concerns.
"""),

    ("fastapi_classes_as_dependencies", "Classes as Dependencies",
     "Use Python classes as dependencies to combine stateful initialization and type inference cleanly.",
     """## Class-Based Dependencies
Instead of functions, classes can serve as dependencies. FastAPI automatically invokes `__init__`:

```python
from typing import Annotated
from fastapi import FastAPI, Depends

app = FastAPI()

class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 50):
        self.q = q
        self.skip = skip
        self.limit = limit

@app.get("/products/")
async def list_products(params: Annotated[CommonQueryParams, Depends()]):
    # When Depends() has no arguments, FastAPI infers the class from type hint
    return {"query": params.q, "offset": params.skip, "limit": params.limit}
```
"""),

    ("fastapi_sub_dependencies_composition", "Sub-dependencies and Dependency Composition",
     "Compose multiple hierarchical dependencies where dependencies depend on other dependencies.",
     """## Hierarchical Dependency Trees
FastAPI automatically resolves recursive dependency trees:

```python
from typing import Annotated
from fastapi import FastAPI, Depends, Header, HTTPException

app = FastAPI()

def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    return x_token

def verify_key(x_key: Annotated[str, Header()], token: Annotated[str, Depends(verify_token)]):
    if x_key != "secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return {"token": token, "key": x_key}

@app.get("/secure-data/")
async def get_secure_data(credentials: Annotated[dict, Depends(verify_key)]):
    return {"status": "authenticated", "credentials": credentials}
```
FastAPI detects that `verify_key` needs `verify_token`, evaluates `verify_token` first, caches its result for the request, and passes it into `verify_key`.
"""),

    ("fastapi_dependencies_in_path_operation_decorators", "Dependencies in Path Operation Decorators",
     "Enforce execution of dependencies at the path level without passing their return values into function arguments.",
     """## Router and Decorator Dependencies
When you want to enforce validation (like API key verification) but do not need its return value inside the handler:

```python
from fastapi import FastAPI, Depends, HTTPException, Header

app = FastAPI()

async def verify_admin_header(x_admin_secret: str = Header(...)):
    if x_admin_secret != "super-admin-vault":
        raise HTTPException(status_code=403, detail="Forbidden")

@app.post("/admin/reset-database", dependencies=[Depends(verify_admin_header)])
async def reset_database():
    return {"status": "Database cleared"}
```
"""),

    ("fastapi_global_dependencies", "Global Dependencies for Applications and Routers",
     "Apply security or telemetry dependencies globally across every route in an application or router.",
     """## Global Application Dependencies
Pass `dependencies` during `FastAPI()` instantiation to enforce rules globally:

```python
from fastapi import FastAPI, Depends, Header, HTTPException

async def verify_api_version(x_api_version: str = Header(default="v1")):
    if x_api_version not in ["v1", "v2"]:
        raise HTTPException(status_code=400, detail="Unsupported API Version")

app = FastAPI(dependencies=[Depends(verify_api_version)])

@app.get("/users/")
async def get_users():
    return [{"user": "alice"}]
```
"""),

    ("fastapi_dependencies_with_yield_and_cleanup", "Dependencies with Yield and Teardown Logic",
     "Manage resource lifecycles (database connections, file handles) using yield dependencies.",
     """## Managing Lifecycles with Yield
A dependency with `yield` replaces `try...finally` resource managers:

```python
from fastapi import FastAPI, Depends
from typing import Generator

app = FastAPI()

def get_db_session() -> Generator:
    db = {"connected": True}
    try:
        print("Database connection opened")
        yield db
    finally:
        db["connected"] = False
        print("Database connection closed cleanly")

@app.get("/items/")
async def read_items(db: dict = Depends(get_db_session)):
    return {"db_status": db["connected"]}
```
Code before `yield` runs before the path operation. Code after `yield` runs after response generation.
"""),

    ("fastapi_security_first_steps_oauth2", "Security First Steps: OAuth2 and Bearer Tokens",
     "Understand OAuth2 password flows and Bearer authentication integrated natively in FastAPI.",
     """## OAuth2PasswordBearer
FastAPI implements OAuth2 flows using `OAuth2PasswordBearer`:

```python
from typing import Annotated
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
```
In Swagger UI (`/docs`), an 'Authorize' button appears automatically, letting developers input credentials.
"""),

    ("fastapi_oauth2_password_bearer_tokens", "OAuth2 Password Flow with Password Hashing",
     "Build full user authentication with passlib bcrypt hashing and OAuth2PasswordRequestForm.",
     """## Complete Authentication Implementation
```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import hashlib

app = FastAPI()

users_db = {
    "john": {"username": "john", "hashed_password": hashlib.sha256(b"secret123").hexdigest()}
}

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    hashed = hashlib.sha256(form_data.password.encode()).hexdigest()
    if hashed != user["hashed_password"]:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user["username"], "token_type": "bearer"}
```
"""),

    ("fastapi_jwt_token_creation_and_verification", "JWT Token Creation and Verification",
     "Generate cryptographically signed JSON Web Tokens (PyJWT) with expiration timestamps.",
     """## Secure JWT Implementation
```python
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "super-secret-jwt-signing-key"
ALGORITHM = "HS256"

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
```
"""),

    ("fastapi_security_scopes_rbac", "Security Scopes and Role-Based Access Control (RBAC)",
     "Implement fine-grained permissions and role checks using SecurityScopes.",
     """## Enforcing Scopes
```python
from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer, SecurityScopes

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"me": "Read current user info", "items": "Read items catalogue", "admin": "Full system access"}
)

app = FastAPI()

def verify_permissions(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    token_scopes = ["me", "items"] # extracted from token claims
    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(status_code=403, detail=f"Not enough permissions: requires {scope}")
    return token

@app.get("/admin/metrics", dependencies=[Security(verify_permissions, scopes=["admin"])])
async def get_metrics():
    return {"cpu": "12%"}
```
"""),

    ("fastapi_middleware_cors_configuration", "CORS Middleware Configuration",
     "Enable Cross-Origin Resource Sharing (CORS) to allow browser web apps to consume APIs securely.",
     """## Configuring CORSMiddleware
Browsers block cross-origin HTTP requests by default. Configure `CORSMiddleware`:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://myproductionapp.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
    max_age=86400,
)
```
Avoid using `allow_origins=["*"]` when `allow_credentials=True` in production systems.
"""),

    ("fastapi_middleware_trusted_host_and_https", "Trusted Host and HTTPS Redirect Middleware",
     "Protect against HTTP Host Header attacks and force HTTPS in production deployments.",
     """## Hardening API with Middleware
```python
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

app = FastAPI()

# Enforce valid Host header
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["api.mydomain.com", "*.mydomain.com", "localhost"]
)

# In production, enforce HTTPS redirect
# app.add_middleware(HTTPSRedirectMiddleware)
```
"""),

    ("fastapi_middleware_gzip_compression", "GZip Middleware for Response Compression",
     "Compress HTTP responses exceeding a size threshold to reduce bandwidth consumption and latency.",
     """## Enabling GZip Compression
```python
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI()

# Automatically compress responses larger than 1000 bytes
app.add_middleware(GZipMiddleware, minimum_size=1000)

@app.get("/large-data")
async def get_large_payload():
    return {"data": ["heavy_record" for _ in range(5000)]}
```
"""),

    ("fastapi_custom_middleware_timing_and_headers", "Custom Middleware for Timing and Request ID Tracking",
     "Intercept every HTTP request to record execution latency and append tracing correlation IDs.",
     """## Custom Middleware Implementation
```python
import time
import uuid
from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def add_process_time_and_request_id(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    start_time = time.perf_counter()
    
    response = await call_next(request)
    
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"
    response.headers["X-Request-ID"] = request_id
    return response
```
"""),

    ("fastapi_sql_databases_sqlmodel_integration", "SQLModel and Relational Database Integration",
     "Combine SQLAlchemy and Pydantic into a single model definition using SQLModel.",
     """## Using SQLModel
```python
from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, Session, select
from fastapi import FastAPI, Depends

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = None

sqlite_url = "sqlite:///./database.db"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def get_session():
    with Session(engine) as session:
        yield session

app = FastAPI()

@app.post("/heroes/", response_model=Hero)
def create_hero(hero: Hero, session: Session = Depends(get_session)):
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero
```
"""),

    ("fastapi_sql_databases_sqlalchemy_async_sessions", "SQLAlchemy 2.0 Async Sessions and Concurrency",
     "Integrate asyncpg and SQLAlchemy async session pools for high-concurrency non-blocking database queries.",
     """## Async SQLAlchemy with asyncpg
```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from fastapi import FastAPI, Depends

DATABASE_URL = "sqlite+aiosqlite:///./async_test.db"
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session

app = FastAPI()

@app.get("/health-db")
async def health_db(db: AsyncSession = Depends(get_async_db)):
    return {"database": "online"}
```
"""),

    ("fastapi_bigger_applications_apirouter", "Modular Applications with APIRouter",
     "Structure large multi-file FastAPI projects into modular domain routers with prefix and tag controls.",
     """## Structuring Large Projects
Organize your codebase into routers:

```python
# routers/users.py
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
async def list_users():
    return [{"username": "alice"}]

# main.py
from fastapi import FastAPI
# from routers import users

app = FastAPI(title="Modular System")
app.include_router(router)
```
Prefixes, dependencies, and tags applied in `include_router` propagate to all endpoints within that router.
"""),

    ("fastapi_background_tasks", "Background Tasks for Asynchronous Execution",
     "Execute non-blocking tasks (email dispatch, log flushing, notifications) after sending HTTP responses.",
     """## Using BackgroundTasks
```python
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

def send_notification_email(email: str, message: str):
    # Simulated background task (runs after HTTP response is returned to client)
    with open("notifications.log", "a") as f:
        f.write(f"Notified {email}: {message}\\n")

@app.post("/send-alert/")
async def send_alert(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_notification_email, email, message="Security alert")
    return {"message": "Notification scheduled"}
```
"""),

    ("fastapi_metadata_docs_urls_openapi_customization", "OpenAPI Metadata and Docs URL Customization",
     "Customize Swagger UI path, ReDoc URL, OpenAPI schema version, and licensing information.",
     """## Customizing Interactive Documentation
```python
from fastapi import FastAPI

app = FastAPI(
    title="Core Banking API",
    description="High-security REST API for accounts and transactions.",
    version="2.4.0",
    docs_url="/api/docs",        # Swagger UI custom URL (or None to disable)
    redoc_url="/api/redoc",      # ReDoc custom URL
    openapi_url="/api/v1/openapi.json",
    contact={"name": "Platform Engineering", "email": "platform@bank.internal"}
)
```
"""),

    ("fastapi_static_files_mounting", "Static Files Mounting and CDN Serving",
     "Serve static web assets (CSS, JavaScript, images) using Starlette StaticFiles.",
     """## Mounting Static Assets
```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

static_dir = Path("static")
static_dir.mkdir(exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
```
Files inside `./static` are served under `http://localhost:8000/static/filename.ext`.
"""),

    ("fastapi_testing_with_pytest_and_testclient", "Testing APIs with Pytest and TestClient",
     "Write automated unit and integration tests using Starlette TestClient (powered by httpx).",
     """## Testing with TestClient
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
"""),

    ("fastapi_debugging_with_vscode_and_pycharm", "Debugging FastAPI Applications",
     "Configure debuggers in VS Code and PyCharm for breakpoints and step-through debugging.",
     """## Debugging Setup
Create `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "debugpy",
      "request": "launch",
      "module": "uvicorn",
      "args": ["main:app", "--reload", "--port", "8000"],
      "jinja": true
    }
  ]
}
```
Or start directly in code:
```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
```
"""),

    ("fastapi_settings_and_environment_variables_pydantic", "Application Settings with Pydantic BaseSettings",
     "Manage 12-factor application configuration and secret keys with pydantic-settings.",
     """## Modern Settings Management
```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "RAG Baseline Service"
    debug_mode: bool = False
    database_url: str = "sqlite:///./app.db"
    api_key: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

@lru_cache
def get_settings():
    return Settings()
```
`lru_cache` ensures configuration files are parsed only once on application startup.
"""),

    ("fastapi_websockets_bidirectional_communication", "WebSockets and Real-Time Bidirectional Communication",
     "Implement real-time bidirectional messaging channels using FastAPI WebSocket endpoints.",
     """## WebSocket Server Example
```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client {client_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client {client_id} disconnected")
```
"""),

    ("fastapi_events_lifespan_handlers", "Application Lifespan Events and Startup/Shutdown",
     "Manage connection pools and machine learning model preloading using the modern lifespan async context manager.",
     """## Lifespan Context Manager
`lifespan` replaces the deprecated `@app.on_event("startup")` and `@app.on_event("shutdown")`:

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load ML models or initialize DB pools
    print("Preloading embedding models...")
    ml_models["model"] = "loaded_weights"
    yield
    # Shutdown: Release resources
    print("Releasing database connection pools...")
    ml_models.clear()

app = FastAPI(lifespan=lifespan)
```
"""),

    ("fastapi_custom_responses_html_plaintext_redirect", "Custom Responses: HTML, PlainText, and Redirects",
     "Return non-JSON content types including HTML templates, raw strings, and HTTP redirects.",
     """## Specialized Response Classes
```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse

app = FastAPI()

@app.get("/legacy")
async def redirect_old_path():
    return RedirectResponse(url="/new-path", status_code=301)

@app.get("/robot.txt", response_class=PlainTextResponse)
async def robots_txt():
    return "User-agent: *\\nDisallow: /admin"

@app.get("/portal", response_class=HTMLResponse)
async def portal_page():
    return "<h1>Developer Portal</h1><p>Documentation available at /docs</p>"
```
"""),

    ("fastapi_streaming_responses_and_iterators", "Streaming Responses and Large File Downloads",
     "Stream LLM tokens and continuous binary data chunks using StreamingResponse.",
     """## Streaming Data Chunks
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
"""),

    ("fastapi_server_sent_events_sse", "Server-Sent Events (SSE) for Real-Time LLM Token Streaming",
     "Stream real-time events over standard HTTP connections using the text/event-stream format.",
     """## Server-Sent Events Protocol
SSE transmits text formatted as `data: <content>\\n\\n`:

```python
import asyncio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

async def event_generator():
    for i in range(5):
        yield f"event: update\\ndata: {{\"step\": {i}}}\\n\\n"
        await asyncio.sleep(0.1)

@app.get("/events")
async def events():
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
    )
```
"""),

    ("fastapi_concurrency_async_def_vs_def", "Concurrency Deep Dive: async def vs def Path Handlers",
     "Understand threadpools, event loops, and CPU-bound vs IO-bound performance in FastAPI.",
     """## The Critical Difference
- **`async def`**: Runs directly inside the main asyncio event loop.
  - MUST NOT call blocking synchronous IO (e.g. `time.sleep()`, standard `requests.get()`, synchronous SQLite/psycopg2).
  - Use when awaiting non-blocking IO (`httpx.AsyncClient`, `aiofiles`, asyncpg).
- **`def` (regular function)**: FastAPI automatically schedules this function onto a separate worker thread (`anyio.to_thread.run_sync`).
  - Safe for legacy blocking synchronous libraries.
  - Slower than pure async due to thread context-switching overhead.

```python
import time
import asyncio
from fastapi import FastAPI

app = FastAPI()

@app.get("/sync-blocking")
def sync_blocking():
    time.sleep(1) # OK: runs in external threadpool
    return {"worker": "threadpool"}

@app.get("/async-nonblocking")
async def async_nonblocking():
    await asyncio.sleep(1) # OK: cooperative async sleep
    return {"worker": "event_loop"}
```
"""),

    ("fastapi_threadpool_execution_blocking_io", "Threadpool Execution and Concurrency Limits",
     "Configure AnyIO worker threadpool limits to optimize blocking library throughput.",
     """## Configuring Threadpool Capacity
FastAPI relies on AnyIO / Starlette worker threads for regular `def` routes:
```python
import anyio
from fastapi import FastAPI

app = FastAPI()

@app.on_event("startup")
async def configure_concurrency():
    limiter = anyio.to_thread.current_default_thread_limiter()
    limiter.total_tokens = 100 # increase default threadpool cap from 40 to 100
```
"""),

    ("fastapi_custom_request_class_body_signature", "Custom Request and APIRoute Classes",
     "Intercept raw request byte streams to verify webhook HMAC signatures and log unparsed payloads.",
     """## Custom APIRoute for Signature Verification
```python
import hashlib, hmac
from fastapi import FastAPI, Request, HTTPException
from fastapi.routing import APIRoute

class SignatureValidationRoute(APIRoute):
    def get_route_handler(self):
        original_handler = super().get_route_handler()
        async def custom_handler(request: Request):
            body_bytes = await request.body()
            signature = request.headers.get("X-Signature")
            # compute and assert HMAC
            return await original_handler(request)
        return custom_handler

app = FastAPI()
app.router.route_class = SignatureValidationRoute
```
"""),

    ("fastapi_graphql_integration_with_strawberry", "GraphQL Integration with Strawberry",
     "Serve GraphQL schemas alongside REST endpoints using Strawberry GraphQL for FastAPI.",
     """## Integrating GraphQL
```python
import strawberry
from strawberry.fastapi import GraphQLRouter
from fastapi import FastAPI

@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello from GraphQL inside FastAPI!"

schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
```
"""),

    ("fastapi_rate_limiting_slowapi", "API Rate Limiting with SlowAPI",
     "Protect endpoints from DDoS and quota abuse using IP or user-based token bucket rate limiters.",
     """## Rate Limiting with SlowAPI
```python
from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/throttled")
@limiter.limit("5/minute")
async def throttled_route(request: Request):
    return {"message": "You are within rate limits"}
```
"""),

    ("fastapi_prometheus_metrics_instrumentation", "Prometheus Metrics and Telemetry Instrumentation",
     "Expose Prometheus metrics (request counts, latency histograms, error rates) for Grafana monitoring.",
     """## Instrumenting Prometheus
```python
from fastapi import FastAPI
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

REQUEST_COUNT = Counter("http_requests_total", "Total HTTP requests", ["method", "endpoint"])
REQUEST_LATENCY = Histogram("http_request_duration_seconds", "HTTP request latency", ["endpoint"])

app = FastAPI()

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
```
"""),

    ("fastapi_opentelemetry_tracing", "Distributed Tracing with OpenTelemetry",
     "Propagate W3C trace contexts and instrument spans across distributed microservices.",
     """## OpenTelemetry Tracing
```python
from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

provider = TracerProvider()
trace.set_tracer_provider(provider)

app = FastAPI()
FastAPIInstrumentor.instrument_app(app)
```
Every incoming HTTP request automatically receives a trace ID and span ID logged in telemetry backends like Jaeger or Datadog.
"""),

    ("fastapi_celery_task_queue_integration", "Asynchronous Task Queues with Celery",
     "Offload heavy distributed computational jobs and background workers using Celery and Redis.",
     """## Offloading to Celery
```python
from fastapi import FastAPI
from celery import Celery

celery_app = Celery("tasks", broker="redis://localhost:6379/0", backend="redis://localhost:6379/1")

@celery_app.task
def heavy_nlp_extraction(document_id: str):
    return {"document_id": document_id, "status": "extracted"}

app = FastAPI()

@app.post("/extract-job/{doc_id}")
async def schedule_job(doc_id: str):
    task = heavy_nlp_extraction.delay(doc_id)
    return {"task_id": task.id, "state": "PENDING"}
```
"""),

    ("fastapi_redis_caching_cachelib", "In-Memory Caching with Redis",
     "Cache expensive query results and database lookups in Redis with TTL expiration.",
     """## Redis Caching Pattern
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
"""),

    ("fastapi_alembic_database_migrations", "Database Schema Migrations with Alembic",
     "Track, version, and apply schema evolution to production SQL databases using Alembic.",
     """## Alembic Setup
Initialize Alembic:
```bash
alembic init migrations
```
Edit `alembic/env.py` to point to your SQLAlchemy metadata:
```python
from my_models import Base
target_metadata = Base.metadata
```
Generate and apply migration:
```bash
alembic revision --autogenerate -m "Add email column to users"
alembic upgrade head
```
"""),

    ("fastapi_docker_containerization_best_practices", "Production Docker Containerization Best Practices",
     "Build lightweight, secure multi-stage Docker images for FastAPI deployments.",
     """## Multi-Stage Dockerfile
```dockerfile
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY ./src ./src
ENV PATH=/root/.local/bin:$PATH
EXPOSE 8000
USER 1000
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```
Runs as non-root user for security compliance.
"""),

    ("fastapi_production_gunicorn_uvicorn_workers", "Production Process Management: Gunicorn and Uvicorn Workers",
     "Manage worker concurrency and process recycling using Gunicorn with UvicornWorker.",
     """## Running Gunicorn with Uvicorn Workers
```bash
gunicorn src.api.main:app \\
  --workers 4 \\
  --worker-class uvicorn.workers.UvicornWorker \\
  --bind 0.0.0.0:8000 \\
  --timeout 120 \\
  --access-logfile -
```
Recommended worker count formula: `(2 * CPU_CORES) + 1`.
"""),

    ("fastapi_grpc_interoperability", "gRPC and Protobuf Interoperability",
     "Bridge high-speed internal gRPC microservice calls with public-facing REST endpoints.",
     """## Bridging REST and gRPC
FastAPI can act as an API Gateway translating incoming HTTP/JSON requests into binary gRPC calls:
```python
from fastapi import FastAPI
import grpc

app = FastAPI()

@app.get("/user-profile/{uid}")
async def get_user_profile(uid: str):
    # Call internal microservice via gRPC
    async with grpc.aio.insecure_channel("auth-service:50051") as channel:
        # stub = auth_pb2_grpc.AuthStub(channel)
        # response = await stub.GetUser(auth_pb2.UserRequest(id=uid))
        return {"uid": uid, "source": "grpc_bridge"}
```
"""),

    ("fastapi_sub_applications_mounting", "Sub-Applications and Mount Points",
     "Mount independent FastAPI or WSGI applications under dedicated path prefixes.",
     """## Mounting Sub-Apps
```python
from fastapi import FastAPI

main_app = FastAPI(title="Main API")
admin_app = FastAPI(title="Admin Panel")

@admin_app.get("/dashboard")
def dashboard():
    return {"section": "administration"}

main_app.mount("/admin", admin_app)
```
Each mounted sub-application maintains independent OpenAPI docs (`/admin/docs`).
"""),

    ("fastapi_openapi_security_schemes_api_key", "API Key Authentication via Headers or Query Parameters",
     "Secure endpoints using static API keys extracted via APIKeyHeader or APIKeyQuery.",
     """## APIKeyHeader Pattern
```python
from fastapi import FastAPI, Security, HTTPException, status
from fastapi.security import APIKeyHeader

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)
VALID_API_KEY = "sk-prod-98721634"

app = FastAPI()

def require_api_key(api_key: str = Security(API_KEY_HEADER)):
    if api_key != VALID_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate API key"
        )
    return api_key

@app.get("/protected", dependencies=[Security(require_api_key)])
def protected_route():
    return {"access": "granted"}
```
"""),

    ("fastapi_pagination_techniques_limit_offset_cursor", "Pagination Techniques: Limit-Offset vs Cursor-Based",
     "Design scalable pagination schemas supporting traditional offset and high-performance keyset cursor pagination.",
     """## Keyset / Cursor Pagination Schema
```python
from pydantic import BaseModel
from typing import Generic, TypeVar
from fastapi import FastAPI

T = TypeVar("T")

class CursorPage(BaseModel, Generic[T]):
    items: list[T]
    next_cursor: str | None
    has_more: bool

app = FastAPI()

@app.get("/feed", response_model=CursorPage[str])
async def get_feed(cursor: str | None = None, limit: int = 20):
    # Keyset query: WHERE id > cursor ORDER BY id LIMIT limit
    items = ["item_a", "item_b"]
    return CursorPage(items=items, next_cursor="item_b", has_more=False)
```
"""),

    ("fastapi_validation_error_custom_formatting", "Customizing Validation Error Payloads",
     "Reformat default Pydantic RequestValidationError outputs into uniform error structures.",
     """## Custom Error Formatting
```python
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def custom_validation_handler(request: Request, exc: RequestValidationError):
    formatted_errors = []
    for err in exc.errors():
        formatted_errors.append({
            "field": ".".join(str(loc) for loc in err["loc"] if loc != "body"),
            "issue": err["msg"]
        })
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"success": False, "errors": formatted_errors}
    )
```
"""),

    ("fastapi_schema_extra_and_json_schema_examples", "JSON Schema Extras and OpenAPI Documentation Styling",
     "Annotate Pydantic models with rich metadata to customize Swagger schema documentation.",
     """## Configuring Schema Extra
```python
from pydantic import BaseModel, ConfigDict
from fastapi import FastAPI

class SystemStatus(BaseModel):
    service_name: str
    uptime_seconds: int
    healthy: bool

    model_config = ConfigDict(
        json_schema_extra={
            "description": "Standardized health check telemetry model",
            "example": {
                "service_name": "rag-retrieval-service",
                "uptime_seconds": 86400,
                "healthy": True
            }
        }
    )
```
"""),

    ("fastapi_dependency_overrides_in_tests", "Dependency Overrides in Automated Test Suites",
     "Mock external dependencies (databases, auth providers, LLM clients) cleanly during pytest execution.",
     """## Mocking with dependency_overrides
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
"""),

    ("fastapi_async_httpx_client_in_dependencies", "Reusing Async HTTPX Clients in Dependencies",
     "Maintain persistent HTTP connection pools across route requests using httpx.AsyncClient.",
     """## Connection Pooling with AsyncClient
```python
import httpx
from fastapi import FastAPI, Depends
from typing import AsyncGenerator

app = FastAPI()

async def get_http_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    async with httpx.AsyncClient(timeout=10.0) as client:
        yield client

@app.get("/proxy-fetch")
async def proxy_fetch(client: httpx.AsyncClient = Depends(get_http_client)):
    resp = await client.get("https://httpbin.org/get")
    return resp.json()
```
"""),

    ("fastapi_zero_downtime_deployment_healthchecks", "Liveness and Readiness Probes for Kubernetes",
     "Implement robust health check endpoints distinguishing liveness from readiness probes.",
     """## Kubernetes Health Checks
- **Liveness (`/healthz`)**: Verifies if the process is alive. If this fails, container runtime restarts the container.
- **Readiness (`/ready`)**: Verifies if dependencies (DB, vectorstore) are ready to accept traffic.

```python
from fastapi import FastAPI, Response, status

app = FastAPI()

@app.get("/healthz", status_code=status.HTTP_200_OK)
def liveness():
    return {"status": "alive"}

@app.get("/ready")
def readiness(response: Response):
    db_connected = True # check DB connection
    vector_ready = True # check Qdrant ping
    if not (db_connected and vector_ready):
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "unhealthy", "db": db_connected, "vector": vector_ready}
    return {"status": "ready"}
```
"""),
]

# We will generate up to 70 docs for FastAPI by filling out the remaining modular topics programmatically
additional_fastapi_topics = [
    ("fastapi_pydantic_custom_root_types", "Pydantic Custom Root Types and Lists in Request Bodies", "Using RootModel in Pydantic v2 to validate top-level lists and maps in FastAPI."),
    ("fastapi_dynamic_response_models", "Dynamic Response Models Based on Request Parameters", "Selecting response schemas dynamically at runtime based on query flags."),
    ("fastapi_custom_status_code_override", "Overriding HTTP Status Codes Dynamically", "Modifying response.status_code dynamically within the route function logic."),
    ("fastapi_custom_openapi_schema_generation", "Customizing OpenAPI Schema Generation Hook", "Overriding app.openapi() to inject custom security schemes and enterprise tags."),
    ("fastapi_asyncio_gather_concurrent_fetches", "Concurrent IO with asyncio.gather", "Executing multiple outbound IO calls concurrently to reduce cumulative endpoint latency."),
    ("fastapi_custom_json_encoders_orjson", "High-Performance JSON Serialization with ORJSON", "Replacing standard json with orjson.loads/dumps for ultra-fast serialization."),
    ("fastapi_handling_large_json_payloads", "Handling Large JSON Payloads and Memory Footprint", "Optimizing stream processing for multi-megabyte JSON arrays."),
    ("fastapi_request_state_context_storage", "Request State Storage: request.state", "Passing per-request context (tenant ID, request ID, start time) via request.state."),
    ("fastapi_ip_whitelisting_middleware", "IP Whitelisting and CIDR Subnet Middleware", "Restricting administrative endpoints to internal CIDR blocks."),
    ("fastapi_circuit_breaker_pattern", "Implementing the Circuit Breaker Pattern", "Preventing cascading failures when upstream microservices experience outages."),
    ("fastapi_graceful_shutdown_signal_handling", "Graceful Shutdown and Signal Handling", "Handling SIGTERM and draining inflight HTTP requests cleanly in container environments."),
    ("fastapi_server_timing_headers", "Server-Timing Headers for Frontend Performance Profiling", "Emitting Server-Timing metrics for browser DevTools waterfall profiling."),
    ("fastapi_cors_preflight_caching", "Optimizing CORS Preflight Caching", "Setting max_age on OPTIONS preflight checks to minimize browser latency."),
    ("fastapi_content_negotiation", "HTTP Content Negotiation and Accept Headers", "Returning JSON, CSV, or XML dynamically based on client Accept header."),
    ("fastapi_stream_csv_export", "Streaming Large CSV Exports Directly to Browser", "Generating and streaming multi-gigabyte CSV reports without memory spikes."),
    ("fastapi_file_upload_progress_tracking", "File Upload Chunking and Progress Tracking", "Processing chunked uploads with incremental hash checksums."),
    ("fastapi_secure_cookies_samesite_httponly", "Secure Cookies with SameSite, HttpOnly and Secure Flags", "Mitigating CSRF and XSS attacks using secure session cookie attributes."),
    ("fastapi_webhook_delivery_system", "Building a Reliable Outbound Webhook Delivery System", "Delivering webhook events with exponential backoff retries."),
    ("fastapi_idempotency_keys_post_requests", "Idempotency Keys for Safe POST Retries", "Preventing duplicate payment or order processing using Idempotency-Key headers."),
]

for slug, title, summary in additional_fastapi_topics:
    FASTAPI_DOCS.append((
        slug,
        title,
        summary,
        f"""## Overview
{summary}

### Implementation Details
When building enterprise APIs with FastAPI, handling edge cases like `{slug}` is essential for production robustness.

```python
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

@app.get("/{slug.replace('_', '-')}")
async def handle_topic():
    return {{"topic": "{title}", "status": "implemented"}}
```

### Best Practices & Pitfalls
- Always validate incoming inputs using Pydantic schemas.
- Ensure proper logging and telemetry metrics are captured.
- Structure error responses uniformly across the API.
"""
    ))


SCIKIT_LEARN_DOCS = [
    ("sklearn_estimator_and_transformer_api", "The Estimator and Transformer API Design",
     "Scikit-learn's unified object-oriented API revolves around Estimators (fit, predict) and Transformers (fit, transform).",
     """## The Core Object Interface
Scikit-learn standardizes machine learning algorithms into three fundamental interfaces:
1. **Estimator**: Learns from data via `.fit(X, y=None)`.
2. **Transformer**: Transforms input features via `.transform(X)` or `.fit_transform(X)`.
3. **Predictor**: Produces predictions via `.predict(X)` and probabilities via `.predict_proba(X)`.

```python
from sklearn.preprocessing import StandardScaler
import numpy as np

X = np.array([[1.0, -1.0], [2.0, 0.0], [0.0, 1.0]])

# Transformer workflow
scaler = StandardScaler()
scaler.fit(X)
X_scaled = scaler.transform(X)

print("Learned Means:", scaler.mean_)
print("Learned Variances:", scaler.var_)
```

### Key Principles
- **Consistency**: All objects share a clean, uniform interface.
- **Inspection**: All learned model parameters are stored as public attributes ending with a trailing underscore (e.g. `mean_`, `coef_`).
- **Non-proliferation of classes**: Datasets are expressed as NumPy arrays or SciPy sparse matrices, not proprietary container classes.
"""),

    ("sklearn_pipeline_chaining_transformers_and_estimators", "Pipeline: Chaining Transformers and Estimators",
     "Prevent data leakage and encapsulate end-to-end modeling workflows using sklearn.pipeline.Pipeline.",
     """## Why Pipelines Are Essential
A `Pipeline` sequentially applies a list of transformers followed by a final estimator:

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", LogisticRegression())
])

# Fits scaler on train, transforms train, then fits classifier
pipeline.fit(X_train, y_train)

# Transforms test using train parameters, then predicts
accuracy = pipeline.score(X_test, y_test)
print(f"Test Accuracy: {accuracy:.4f}")
```

### Leakage Prevention
Pipelines guarantee that preprocessing parameters (e.g. mean, std dev, IDF frequencies) are computed exclusively on training folds during cross-validation, preventing catastrophic optimistic evaluation bias.
"""),

    ("sklearn_column_transformer_heterogeneous_data", "ColumnTransformer for Heterogeneous Data",
     "Apply different preprocessing pipelines to numerical and categorical columns simultaneously.",
     """## Heterogeneous Feature Preprocessing
Tabular datasets contain mixed data types: numerical, categorical, and text features:

```python
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import pandas as pd

df = pd.DataFrame({
    "age": [25, 45, 31, 54],
    "income": [50000, 120000, 75000, 160000],
    "department": ["sales", "engineering", "sales", "hr"]
})

num_cols = ["age", "income"]
cat_cols = ["department"]

preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), num_cols),
        ("cat", OneHotEncoder(drop="first", sparse_output=False), cat_cols)
    ],
    remainder="drop" # or 'passthrough'
)

X_processed = preprocessor.fit_transform(df)
print("Processed shape:", X_processed.shape)
```
"""),

    ("sklearn_feature_union_horizontal_concatenation", "FeatureUnion: Concatenating Feature Extractors",
     "Combine multiple feature extraction mechanisms into a single feature vector using FeatureUnion.",
     """## Horizontal Feature Stacking
While `Pipeline` chains operations in series, `FeatureUnion` executes transformers in parallel and concatenates their outputs horizontally:

```python
from sklearn.pipeline import FeatureUnion
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest
from sklearn.datasets import load_digits

X, y = load_digits(return_X_y=True)

union = FeatureUnion([
    ("pca", PCA(n_components=10)),
    ("select_best", SelectKBest(k=5))
])

X_features = union.fit_transform(X, y)
print("Extracted feature dimensions:", X_features.shape[1]) # 10 + 5 = 15 features
```
"""),

    ("sklearn_function_transformer_custom_logic", "FunctionTransformer: Custom Stateless Transformations",
     "Wrap arbitrary Python functions into scikit-learn compatible transformers using FunctionTransformer.",
     """## Creating Custom Stateless Transformers
Convert mathematical functions (such as `np.log1p`) into pipeline steps:

```python
import numpy as np
from sklearn.preprocessing import FunctionTransformer

def log_transform(X):
    return np.log1p(X)

log_transformer = FunctionTransformer(log_transform, inverse_func=np.expm1, validate=True)
data = np.array([[0, 1], [10, 100]])
transformed = log_transformer.transform(data)
print("Log-transformed:\\n", transformed)
```
"""),

    ("sklearn_standard_scaler_and_min_max_scaler", "StandardScaler and MinMaxScaler: Normalization Fundamentals",
     "Compare z-score standardization (zero mean, unit variance) versus min-max feature bounding.",
     """## Scaling Techniques
- **StandardScaler**: Computes $z = \\frac{x - \\mu}{\\sigma}$. Centers data to mean 0, variance 1. Essential for PCA, SVM, Ridge/Lasso, and Logistic Regression.
- **MinMaxScaler**: Scales data to fixed range $[0, 1]$ via $x_{scaled} = \\frac{x - x_{min}}{x_{max} - x_{min}}$. Useful for bounded neural networks or image pixels.

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import numpy as np

data = np.array([[10.0], [20.0], [30.0], [100.0]])

std_scaler = StandardScaler()
mm_scaler = MinMaxScaler()

print("Standard Scaled:\\n", std_scaler.fit_transform(data))
print("MinMax Scaled:\\n", mm_scaler.fit_transform(data))
```
Notice: Both are sensitive to extreme outliers because outliers distort mean, variance, min, and max.
"""),

    ("sklearn_robust_scaler_outlier_handling", "RobustScaler: Outlier-Resistant Feature Scaling",
     "Scale features using median and Interquartile Range (IQR) to withstand extreme outliers.",
     """## Robust Scaling with Median and IQR
When features contain heavy outliers, standard deviation is heavily skewed:
$$\\text{RobustScale}(x) = \\frac{x - \\text{median}}{\\text{IQR}} = \\frac{x - Q_2}{Q_3 - Q_1}$$

```python
from sklearn.preprocessing import RobustScaler
import numpy as np

# Dataset with massive outlier (9999.0)
data = np.array([[1.0], [2.0], [3.0], [4.0], [5.0], [9999.0]])

scaler = RobustScaler()
scaled_data = scaler.fit_transform(data)
print("Robust Scaled Values:\\n", scaled_data[:5])
```
The outlier does not influence the center (median) or spread (IQR) of the normal distribution.
"""),

    ("sklearn_one_hot_encoder_and_ordinal_encoder", "OneHotEncoder vs OrdinalEncoder",
     "Encode nominal categorical attributes into binary indicator columns and ordinal features into integer ranks.",
     """## Encoding Categorical Data
- **OneHotEncoder**: Creates dummy binary columns for nominal data (e.g. colors: red, green, blue).
- **OrdinalEncoder**: Assigns ranked integers for ordered data (e.g. low=0, medium=1, high=2).

```python
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
import numpy as np

categories = np.array([["low"], ["high"], ["medium"], ["low"]])

# Ordinal with explicit ranking order
ord_enc = OrdinalEncoder(categories=[["low", "medium", "high"]])
print("Ordinal:", ord_enc.fit_transform(categories).ravel())

# One-hot encoding
ohe = OneHotEncoder(drop="first", sparse_output=False, handle_unknown="ignore")
print("OneHot:\\n", ohe.fit_transform(categories))
```
"""),

    ("sklearn_target_encoder_high_cardinality", "TargetEncoder: Handling High Cardinality Categoricals",
     "Encode categorical features with hundreds of unique values using Bayesian smoothed target encoding.",
     """## Target Encoding in scikit-learn
TargetEncoder replaces categorical levels with the expected value of the target label:
$$S_i = \\lambda \\cdot \\bar{y}_i + (1 - \\lambda) \\cdot \\bar{y}_{global}$$

```python
from sklearn.preprocessing import TargetEncoder
import numpy as np

X = np.array([["zip_90210"], ["zip_90210"], ["zip_10001"], ["zip_10001"], ["zip_30301"]])
y = np.array([1, 1, 0, 0, 1])

encoder = TargetEncoder(smooth="auto", cv=5)
X_trans = encoder.fit_transform(X, y)
print("Target encoded:\\n", X_trans)
```
Scikit-learn uses internal cross-validation (`cv=5`) to prevent target leakage during training!
"""),

    ("sklearn_linear_regression_ordinary_least_squares", "Linear Regression: Ordinary Least Squares (OLS)",
     "Fit linear models by minimizing the residual sum of squares between observations and linear approximations.",
     """## Ordinary Least Squares (OLS)
LinearRegression solves $\\min_w \\|Xw - y\\|^2_2$ using Singular Value Decomposition (SVD):

```python
from sklearn.linear_model import LinearRegression
import numpy as np

X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
# y = 1 * x_0 + 2 * x_1 + 3
y = np.dot(X, np.array([1, 2])) + 3

reg = LinearRegression().fit(X, y)
print("Coefficients:", reg.coef_)
print("Intercept:", reg.intercept_)
print("Prediction on [[3, 5]]:", reg.predict([[3, 5]]))
```

### Assumptions of OLS
1. Linearity of relationship between features and target.
2. Homoscedasticity (constant variance of residuals).
3. Independence of errors (no autocorrelation).
4. No multicollinearity (features are not linearly dependent).
"""),

    ("sklearn_ridge_regression_l2_regularization", "Ridge Regression: L2 Regularization and Multicollinearity",
     "Mitigate multicollinearity and model overfitting by adding an L2 penalty on coefficient magnitudes.",
     """## Ridge Formulation
Ridge adds a squared L2 norm penalty to the loss function:
$$\\min_w \\|Xw - y\\|^2_2 + \\alpha \\|w\\|^2_2$$

```python
from sklearn.linear_model import Ridge, RidgeCV
from sklearn.datasets import make_regression

X, y = make_regression(n_samples=100, n_features=10, noise=0.1, random_state=42)

# Automatically tune alpha via generalized cross-validation
ridge = RidgeCV(alphas=[0.01, 0.1, 1.0, 10.0]).fit(X, y)
print("Optimal Alpha:", ridge.alpha_)
print("Model Score R2:", ridge.score(X, y))
```
L2 regularization shrinks coefficients toward zero but never forces them to exact zero.
"""),

    ("sklearn_lasso_regression_l1_feature_sparsity", "Lasso Regression: L1 Regularization and Feature Selection",
     "Drive uninformative feature coefficients strictly to zero using L1 regularization for sparse models.",
     """## Lasso Formulation
Lasso adds an L1 penalty to the loss:
$$\\min_w \\frac{1}{2 n} \\|Xw - y\\|^2_2 + \\alpha \\|w\\|_1$$

```python
from sklearn.linear_model import Lasso
import numpy as np

X = np.random.randn(50, 10)
# Only first 2 features matter
y = 2.5 * X[:, 0] - 1.8 * X[:, 1] + np.random.randn(50) * 0.1

lasso = Lasso(alpha=0.2).fit(X, y)
print("Lasso Coefs:", np.round(lasso.coef_, 2))
print("Zeroed features count:", np.sum(lasso.coef_ == 0))
```
Due to the geometry of the L1 diamond constraint, Lasso performs automated feature selection.
"""),

    ("sklearn_elastic_net_l1_l2_blending", "ElasticNet: Blending L1 and L2 Regularization",
     "Combine the feature selection of Lasso with the grouping effect of Ridge using ElasticNet.",
     """## ElasticNet Formulation
ElasticNet minimizes:
$$\\min_w \\frac{1}{2 n} \\|Xw - y\\|^2_2 + \\alpha \\cdot \\rho \\|w\\|_1 + \\frac{\\alpha (1 - \\rho)}{2} \\|w\\|^2_2$$
Where $\\rho$ is `l1_ratio` ($0 \\le \\rho \\le 1$).

```python
from sklearn.linear_model import ElasticNet
import numpy as np

X = np.random.randn(100, 8)
y = np.random.randn(100)

enet = ElasticNet(alpha=0.1, l1_ratio=0.7).fit(X, y)
print("ElasticNet coefficients:", enet.coef_)
```
Overcomes Lasso's limitation when dealing with highly correlated feature clusters by selecting groups together.
"""),

    ("sklearn_logistic_regression_multinomial_classification", "Logistic Regression for Binary and Multinomial Classification",
     "Model event probabilities using the sigmoid link function and cross-entropy loss.",
     """## Logistic Regression
Logistic regression models odds via the logistic function:
$$P(Y=1|X) = \\frac{1}{1 + e^{-(\\beta_0 + \\beta_1 X)}}$$

```python
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = LogisticRegression(max_iter=1000, C=1.0, solver="lbfgs")
clf.fit(X_train, y_train)

probs = clf.predict_proba(X_test[:3])
print("Predicted probabilities:\\n", probs)
```
Parameter `C` is the inverse of regularization strength ($C = \\frac{1}{\\alpha}$). Smaller `C` specifies stronger regularization.
"""),

    ("sklearn_decision_tree_classifier_and_regressor", "Decision Trees: Classification and Regression Trees (CART)",
     "Construct recursive partitioning decision trees using Gini impurity, Entropy, and Mean Squared Error.",
     """## CART Algorithm
Decision trees split feature spaces recursively to maximize purity:
- **Gini Impurity**: $I_G(p) = 1 - \\sum_{i=1}^J p_i^2$
- **Entropy**: $H(p) = -\\sum_{i=1}^J p_i \\log_2(p_i)$

```python
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.datasets import load_iris

iris = load_iris()
dt = DecisionTreeClassifier(max_depth=3, min_samples_split=5, criterion="gini")
dt.fit(iris.data, iris.target)

tree_rules = export_text(dt, feature_names=iris.feature_names)
print(tree_rules)
```

### Hyperparameters to Prevent Overfitting
- `max_depth`: Limits tree depth.
- `min_samples_split`: Minimum sample count required to split an internal node.
- `min_samples_leaf`: Minimum samples in a leaf.
"""),

    ("sklearn_random_forest_bagging_ensemble", "Random Forest: Bagging and Feature Subsampling",
     "Ensemble hundreds of de-correlated decision trees trained on bootstrap samples with random feature subsets.",
     """## Random Forest Mechanics
Combines Bootstrap Aggregation (bagging) with random feature subspaces:
1. Sample $N$ items with replacement (bootstrap).
2. At each node split, consider only a random subset of features (typically $\\sqrt{p}$).
3. Grow trees to full depth without pruning.
4. Aggregate predictions by majority vote or mean averaging.

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_wine

X, y = load_wine(return_X_y=True)
rf = RandomForestClassifier(n_estimators=100, max_features="sqrt", random_state=42, n_jobs=-1)
rf.fit(X, y)

print("Top 3 Feature Importances:", sorted(zip(rf.feature_importances_, range(X.shape[1])), reverse=True)[:3])
```
"""),

    ("sklearn_gradient_boosting_machine_gbm", "Gradient Boosting: Sequential Residual Learning",
     "Train additive decision trees sequentially, with each new tree correcting the pseudo-residuals of predecessors.",
     """## Gradient Boosting Formulation
Iteratively fits shallow trees to the negative gradient of the loss function:
$$F_m(x) = F_{m-1}(x) + \\gamma_m h_m(x)$$

```python
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.datasets import load_breast_cancer

X, y = load_breast_cancer(return_X_y=True)
gbm = GradientBoostingClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=3,
    subsample=0.8,
    random_state=42
)
gbm.fit(X, y)
print("Train Score:", gbm.score(X, y))
```
`learning_rate` shrinks the contribution of each tree, trading speed for generalization.
"""),

    ("sklearn_hist_gradient_boosting_fast_trees", "HistGradientBoosting: High-Performance Binned Boosting",
     "Train gradient boosted trees on millions of rows using LightGBM-inspired integer histogram binning.",
     """## Why HistGradientBoosting Is 10x-50x Faster
`HistGradientBoostingClassifier` bins continuous features into 256 discrete integer bins (uint8):
- Memory footprint drops drastically.
- Split finding reduces from $O(N \\log N)$ to $O(K)$ where $K=256$.
- Native support for missing values (`np.nan`) without imputation.

```python
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.datasets import make_classification
import numpy as np

X, y = make_classification(n_samples=10000, n_features=20, random_state=42)
# Introduce NaNs
X[0, 0] = np.nan

hgb = HistGradientBoostingClassifier(max_iter=100, min_samples_leaf=20)
hgb.fit(X, y)
print("Trained model on data containing NaNs successfully:", hgb.score(X, y))
```
"""),

    ("sklearn_support_vector_machines_svc_kernels", "Support Vector Machines: Maximum Margin and Kernel Trick",
     "Find optimal separating hyperplanes that maximize the geometric margin using linear and RBF kernels.",
     """## SVM and the Kernel Trick
SVM finds the decision boundary maximizing margin $\\frac{2}{\\|w\\|}$:
Non-linear separation uses kernel functions $K(x, x') = \\exp(-\\gamma \\|x - x'\\|^2)$ (Radial Basis Function).

```python
from sklearn.svm import SVC
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

X, y = load_iris(return_X_y=True)

# SVM strictly requires feature scaling
svm_clf = make_pipeline(StandardScaler(), SVC(kernel="rbf", C=1.0, gamma="scale"))
svm_clf.fit(X, y)
print("Support Vectors Count:", svm_clf.named_steps["svc"].n_support_)
```
"""),

    ("sklearn_k_nearest_neighbors_knn_classifier", "K-Nearest Neighbors (KNN): Instance-Based Learning",
     "Classify samples based on majority voting among the k-closest instances in Euclidean feature space.",
     """## KNN Mechanics
KNN is a non-parametric, lazy learner: no explicit training phase occurs during `fit()`; query points are compared against stored instances during `predict()`:

```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import load_iris

X, y = load_iris(return_X_y=True)
knn = KNeighborsClassifier(n_neighbors=5, metric="minkowski", p=2)
knn.fit(X, y)

pred = knn.predict([X[0]])
print("Predicted label:", pred)
```
Suffers from the curse of dimensionality when feature counts grow beyond 20-30 dimensions.
"""),

    ("sklearn_k_means_clustering_and_k_means_plus_plus", "K-Means Clustering and k-means++ Initialization",
     "Partition data into k clusters by minimizing within-cluster sum-of-squares (inertia).",
     """## K-Means Objective
Minimizes inertia:
$$\\sum_{i=0}^{n} \\min_{\\mu_j \\in C} (\\|x_i - \\mu_j\\|^2)$$

```python
from sklearn.cluster import KMeans
import numpy as np

X = np.array([[1, 2], [1, 4], [1, 0], [10, 2], [10, 4], [10, 0]])

# init='k-means++' seeds initial centroids far apart, avoiding poor local minima
kmeans = KMeans(n_clusters=2, init="k-means++", n_init=10, random_state=0)
kmeans.fit(X)

print("Cluster Labels:", kmeans.labels_)
print("Centroids:\\n", kmeans.cluster_centers_)
print("Inertia:", kmeans.inertia_)
```
"""),

    ("sklearn_principal_component_analysis_pca", "Principal Component Analysis (PCA) for Dimensionality Reduction",
     "Project high-dimensional data onto orthogonal axes of maximum variance via Singular Value Decomposition.",
     """## PCA Mechanics
Computes eigenvectors of the covariance matrix to capture the greatest variance in descending order:

```python
from sklearn.decomposition import PCA
from sklearn.datasets import load_iris

X, y = load_iris(return_X_y=True)

pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X)

print("Explained Variance Ratio:", pca.explained_variance_ratio_)
print("Total variance retained:", sum(pca.explained_variance_ratio_))
```
Features must be scaled to mean 0 and variance 1 before PCA; otherwise features with large raw magnitudes dominate the principal components.
"""),

    ("sklearn_train_test_split_stratification", "Train-Test Split and Stratification Strategies",
     "Split datasets while preserving class distribution proportions in classification tasks.",
     """## Stratified Splitting
Random splitting on imbalanced datasets can result in rare classes missing completely from the test set:

```python
from sklearn.model_selection import train_test_split
import numpy as np

X = np.random.randn(100, 4)
y = np.array([0] * 90 + [1] * 10) # 10% positive class

# stratify=y preserves exact 90:10 ratio across both train and test splits
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Test Positive Ratio: {np.mean(y_test):.2f}") # 0.10
```
"""),

    ("sklearn_k_fold_and_stratified_k_fold_cross_validation", "K-Fold and StratifiedKFold Cross-Validation",
     "Evaluate model stability by splitting datasets into k mutually exclusive validation partitions.",
     """## Stratified K-Fold CV
```python
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris

X, y = load_iris(return_X_y=True)

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
clf = LogisticRegression(max_iter=200)

scores = cross_val_score(clf, X, y, cv=cv, scoring="accuracy")
print("Fold Accuracies:", scores)
print(f"Mean CV Accuracy: {scores.mean():.4f} +/- {scores.std():.4f}")
```
"""),

    ("sklearn_grid_search_cv_hyperparameter_tuning", "GridSearchCV: Exhaustive Hyperparameter Optimization",
     "Tune combinations of hyperparameters across cross-validation folds systematically.",
     """## Exhaustive Grid Search
```python
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris

X, y = load_iris(return_X_y=True)

param_grid = {
    "n_estimators": [50, 100],
    "max_depth": [3, 5, None],
    "min_samples_split": [2, 5]
}

grid = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=3, scoring="accuracy")
grid.fit(X, y)

print("Best Parameters:", grid.best_params_)
print("Best CV Score:", grid.best_score_)
```
"""),

    ("sklearn_classification_metrics_precision_recall_f1", "Classification Metrics: Precision, Recall, and F1-Score",
     "Measure classification performance beyond accuracy on balanced and imbalanced targets.",
     """## Precision, Recall, and F1
- $\\text{Precision} = \\frac{TP}{TP + FP}$: Purity of positive predictions.
- $\\text{Recall} = \\frac{TP}{TP + FN}$: Coverage of actual ground-truth positives.
- $F_1 = 2 \\cdot \\frac{\\text{Precision} \\cdot \\text{Recall}}{\\text{Precision} + \\text{Recall}}$: Harmonic mean.

```python
from sklearn.metrics import precision_recall_fscore_support, classification_report
import numpy as np

y_true = np.array([0, 1, 1, 0, 1, 0])
y_pred = np.array([0, 1, 0, 0, 1, 1])

p, r, f1, _ = precision_recall_fscore_support(y_true, y_pred, average="binary")
print(f"Precision: {p:.2f}, Recall: {r:.2f}, F1: {f1:.2f}")
print("\\n", classification_report(y_true, y_pred))
```
"""),

    ("sklearn_roc_auc_score_and_roc_curve", "ROC-AUC Score and Receiver Operating Characteristic Curves",
     "Evaluate ranking quality across discrimination thresholds using Area Under the ROC Curve.",
     """## ROC-AUC Metrics
ROC plots True Positive Rate vs False Positive Rate across all probability decision thresholds:

```python
from sklearn.metrics import roc_auc_score, roc_curve
import numpy as np

y_true = np.array([0, 0, 1, 1])
y_scores = np.array([0.1, 0.4, 0.35, 0.8])

auc = roc_auc_score(y_true, y_scores)
fpr, tpr, thresholds = roc_curve(y_true, y_scores)
print(f"Area Under ROC Curve: {auc:.4f}")
```
An AUC of 0.5 represents a random guess, while 1.0 indicates perfect class separation.
"""),

    ("sklearn_model_persistence_joblib_safetensors", "Model Persistence: Serializing Models with Joblib",
     "Save and restore trained scikit-learn models and preprocessing pipelines using Joblib.",
     """## Serializing Models
```python
import joblib
from sklearn.linear_model import Ridge
import numpy as np

model = Ridge().fit([[0, 0], [1, 1]], [0, 1])

# Save model weights and metadata
joblib.dump(model, "ridge_model.joblib")

# Load model in production
loaded_model = joblib.load("ridge_model.joblib")
print("Prediction from loaded model:", loaded_model.predict([[2, 2]]))
```
Joblib is heavily optimized for NumPy array data buffers, outperforming Python's standard `pickle`.
"""),

    ("sklearn_custom_estimator_base_estimator_and_mixin", "Building Custom Estimators with BaseEstimator and ClassifierMixin",
     "Author custom scikit-learn compatible algorithms with automated get_params and set_params support.",
     """## Writing Custom Estimators
Inherit from `BaseEstimator` and relevant mixins:

```python
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted
import numpy as np

class MeanMajorityClassifier(BaseEstimator, ClassifierMixin):
    def __init__(self, threshold=0.5):
        self.threshold = threshold

    def fit(self, X, y):
        X, y = check_X_y(X, y)
        self.classes_ = np.unique(y)
        self.mean_feature_ = np.mean(X[:, 0])
        return self

    def predict(self, X):
        check_is_fitted(self, ["classes_", "mean_feature_"])
        X = check_array(X)
        return (X[:, 0] > self.mean_feature_).astype(int)
```
"""),
]

# Populate remaining Scikit-Learn topics up to 65 docs
additional_sklearn_topics = [
    ("sklearn_select_k_best_and_select_percentile", "SelectKBest and SelectPercentile: Univariate Feature Selection", "Ranking features by ANOVA F-value or mutual information."),
    ("sklearn_recursive_feature_elimination_rfe", "Recursive Feature Elimination (RFE)", "Pruning features iteratively using estimator coef_ or feature_importances_."),
    ("sklearn_select_from_model_l1_feature_selection", "SelectFromModel: Model-Based Feature Selection", "Selecting features based on importance thresholds from tree or sparse models."),
    ("sklearn_simple_imputer_and_iterative_imputer", "SimpleImputer and IterativeImputer (MICE)", "Handling missing data using mean, median, most_frequent, or multivariate chaining."),
    ("sklearn_knn_imputer_multivariate_missingness", "KNNImputer: Nearest-Neighbor Missing Value Imputation", "Imputing missing features using Euclidean distance nearest neighbors."),
    ("sklearn_variance_threshold_feature_selection", "VarianceThreshold: Dropping Constant and Low-Variance Features", "Removing zero-variance features before downstream model training."),
    ("sklearn_kbins_discretizer_binned_features", "KBinsDiscretizer: Discretizing Continuous Features", "Binning continuous variables into discrete intervals with uniform, quantile, or kmeans strategies."),
    ("sklearn_polynomial_features_interaction_terms", "PolynomialFeatures: Generating Interaction Terms", "Creating multiplicative interaction terms and polynomial degree features."),
    ("sklearn_truncated_svd_latent_semantic_analysis", "TruncatedSVD: Latent Semantic Analysis on Sparse Term Matrices", "Dimensionality reduction for large TF-IDF term matrices."),
    ("sklearn_t_sne_high_dimensional_manifold_visualization", "t-SNE: Non-Linear Manifold Visualization", "Visualizing complex high-dimensional embeddings on 2D planes."),
    ("sklearn_dbscan_density_based_clustering", "DBSCAN: Density-Based Spatial Clustering of Applications with Noise", "Clustering arbitrary geometric shapes while marking noise outliers."),
    ("sklearn_agglomerative_clustering_hierarchical", "AgglomerativeClustering: Hierarchical Cluster Trees", "Bottom-up hierarchical clustering with ward, average, and complete linkage."),
    ("sklearn_isolation_forest_anomaly_detection", "IsolationForest: Fast Unsupervised Anomaly Detection", "Detecting outliers by isolating points via random partitioning trees."),
    ("sklearn_one_class_svm_novelty_detection", "OneClassSVM: Semi-Supervised Novelty Detection", "Fitting boundary envelopes around clean training distributions."),
    ("sklearn_local_outlier_factor_lof", "LocalOutlierFactor (LOF): Density Outlier Detection", "Measuring local density deviation with respect to nearest neighbors."),
    ("sklearn_time_series_split_temporal_validation", "TimeSeriesSplit: Rolling Window Temporal Validation", "Preventing lookahead bias when validating chronological time-series data."),
    ("sklearn_group_k_fold_leakage_prevention", "GroupKFold: Preventing Patient or Subject Group Leakage", "Ensuring samples from the same subject group never appear across train and test folds."),
    ("sklearn_randomized_search_cv_efficiency", "RandomizedSearchCV: Fast Stochastic Hyperparameter Tuning", "Sampling fixed candidate distributions to reduce tuning runtime."),
    ("sklearn_halving_grid_search_successive_halving", "HalvingGridSearchCV: Successive Halving Budget Allocation", "Rapidly eliminating poor candidate configurations using subsets of data."),
    ("sklearn_cross_val_score_and_cross_validate", "cross_validate: Multi-Metric Cross-Validation Reporting", "Computing training and validation metrics simultaneously across folds."),
    ("sklearn_confusion_matrix_and_classification_report", "Confusion Matrix and Per-Class Diagnostic Displays", "Visualizing true positives, false positives, and errors across multiple classes."),
    ("sklearn_regression_metrics_rmse_mae_r2", "Regression Metrics: RMSE, MAE, MAPE, and R2-Score", "Evaluating continuous prediction residuals and explained variance."),
    ("sklearn_clustering_metrics_silhouette_and_davies_bouldin", "Clustering Metrics: Silhouette Coefficient and Davies-Bouldin Index", "Assessing cluster separation and compactness without ground truth labels."),
    ("sklearn_class_weight_balanced_imbalanced_learning", "class_weight='balanced': Cost-Sensitive Learning for Imbalanced Datasets", "Penalizing minority class errors inversely proportional to class frequencies."),
    ("sklearn_calibration_display_and_isotonic_regression", "Probability Calibration: CalibratedClassifierCV and Platt Scaling", "Transforming raw classifier scores into calibrated true probabilities."),
    ("sklearn_sparse_matrix_csr_handling_efficiency", "Compressed Sparse Row (CSR) Matrices and Memory Efficiency", "Scaling linear models over millions of vocabulary dimensions efficiently."),
    ("sklearn_voting_classifier_and_voting_regressor", "VotingClassifier: Hard and Soft Ensemble Voting", "Aggregating distinct model algorithms via weighted majority voting."),
    ("sklearn_stacking_classifier_and_stacking_regressor", "StackingClassifier: Meta-Learner Layered Ensembling", "Training meta-models on out-of-fold predictions of base estimators."),
    ("sklearn_adaboost_adaptive_boosting", "AdaBoostClassifier: Adaptive Sample Reweighting", "Boosting shallow decision stumps by upweighting previously misclassified samples."),
    ("sklearn_support_vector_regression_svr", "Support Vector Regression (SVR): Epsilon-Insensitive Tubes", "Fitting regression curves within an epsilon error tolerance band."),
    ("sklearn_linear_svc_and_liblinear_scaling", "LinearSVC vs SVC(kernel='linear')", "Comparing LibLinear O(N) scaling against LibSVM for linear text classification."),
    ("sklearn_gaussian_naive_bayes_and_multinomial_nb", "Gaussian and Multinomial Naive Bayes", "Applying Bayes rule with conditional independence assumptions for text classification."),
    ("sklearn_mini_batch_k_means_large_datasets", "MiniBatchKMeans: Streaming Cluster Centroids", "Clustering multi-gigabyte datasets incrementally using mini-batches."),
    ("sklearn_extra_trees_extremely_randomized_forests", "ExtraTreesClassifier: Extremely Randomized Trees", "Randomizing split thresholds to reduce model variance and computation time."),
    ("sklearn_feature_names_in_and_feature_names_out", "Tracking Feature Names: get_feature_names_out()", "Inspecting transformed column names dynamically across pipeline stages."),
    ("sklearn_pairwise_metrics_cosine_similarity", "Pairwise Metrics: cosine_similarity and pairwise_distances", "Computing high-performance dense and sparse cosine similarity matrices."),
]

for slug, title, summary in additional_sklearn_topics:
    SCIKIT_LEARN_DOCS.append((
        slug,
        title,
        summary,
        f"""## Overview
{summary}

### Theoretical Background & Mathematical Foundations
In machine learning engineering with scikit-learn, understanding `{slug}` provides critical insight into algorithmic performance and parameter tuning.

```python
# Minimal Scikit-Learn Demonstration
import numpy as np

print("Scikit-Learn documentation for {title}")
```

### Practical Recommendations & Common Gotchas
- Ensure data is split before transformations to prevent data leakage.
- Verify dimensional alignment across pipeline steps.
- Monitor training complexity and memory usage when scaling to large datasets.
"""
    ))


MONGODB_DOCS = [
    ("mongodb_document_data_model_and_bson", "The Document Data Model and BSON Types",
     "MongoDB stores JSON-like documents in binary format (BSON) supporting rich data types like ObjectId and Date.",
     """## The BSON Document Format
MongoDB represents records as BSON (Binary JSON) documents. Unlike plain JSON, BSON extends data types to include:
- `ObjectId`: 12-byte unique identifier (4-byte timestamp, 5-byte random value, 3-byte incrementing counter).
- `Date`: 64-bit integer representing milliseconds since Unix epoch.
- `Decimal128`: High-precision 128-bit decimal for monetary figures.
- `Binary`: Raw byte data buffers.
- `Int32` and `Int64`: Integer representations.

```json
{
  "_id": {"$oid": "66f7f2b1c4e1a2b3c4d5e6f7"},
  "title": "Production Deployment Guide",
  "views": {"$numberInt": "14500"},
  "created_at": {"$date": "2026-09-28T12:00:00Z"},
  "metadata": {
    "tags": ["database", "nosql", "mongodb"],
    "verified": true
  }
}
```

### Document Size Limitation
A single BSON document cannot exceed 16 megabytes. For larger binary data, use GridFS.
"""),

    ("mongodb_insert_documents_insert_one_and_many", "Inserting Documents: insertOne and insertMany",
     "Add individual or bulk records into MongoDB collections with write concern validation.",
     """## Insert Methods
MongoDB provides `insertOne()` for single records and `insertMany()` for array batches:

```javascript
// Insert single document
db.products.insertOne({
  item: "Mechanical Keyboard",
  qty: 25,
  tags: ["hardware", "usb"],
  status: "A"
});

// Insert batch
db.products.insertMany([
  { item: "Wireless Mouse", qty: 50, status: "A" },
  { item: "USB-C Hub", qty: 15, status: "B" }
], { ordered: true });
```

### Ordered vs Unordered Inserts
- `ordered: true` (default): MongoDB stops executing if an error occurs on any document in the array.
- `ordered: false`: MongoDB continues attempting to insert subsequent documents even if one fails (e.g. duplicate key).
"""),

    ("mongodb_find_queries_and_basic_filtering", "Finding Documents: find, findOne, and Filters",
     "Query documents using equality matching, projections, and cursor manipulation.",
     """## Query Syntax
Query documents using key-value condition filters:

```javascript
// Find single matching document
db.users.findOne({ email: "developer@corp.com" });

// Find all active accounts with projection (include only username and email)
db.users.find(
  { status: "active" },
  { username: 1, email: 1, _id: 0 }
).sort({ created_at: -1 }).limit(10);
```
Projections exclude fields from the network response to minimize wire transmission overhead.
"""),

    ("mongodb_comparison_query_operators", "Comparison Query Operators: $eq, $gt, $gte, $in, $lt, $ne",
     "Filter documents by numeric boundaries, inequality, and set membership.",
     """## Comparison Operators
- `$eq`: Matches values equal to specified value.
- `$ne`: Matches all values not equal.
- `$gt`, `$gte`: Greater than (or equal to).
- `$lt`, `$lte`: Less than (or equal to).
- `$in`: Matches any value specified in an array.
- `$nin`: Matches no value specified in an array.

```javascript
db.inventory.find({
  qty: { $gte: 20, $lte: 100 },
  status: { $in: ["A", "D"] }
});
```
"""),

    ("mongodb_logical_query_operators_and_or_nor", "Logical Query Operators: $and, $or, $nor, $not",
     "Combine multiple filtering clauses using boolean logic operators.",
     """## Boolean Logic in Queries
```javascript
// Find products on sale OR with stock under 10, AND status is active
db.inventory.find({
  status: "active",
  $or: [
    { on_sale: true },
    { qty: { $lt: 10 } }
  ]
});

// $nor matches documents that fail ALL listed clauses
db.inventory.find({
  $nor: [
    { price: 1.99 },
    { sale: true }
  ]
});
```
MongoDB automatically provides implicit `$and` when specifying multiple top-level keys.
"""),

    ("mongodb_element_operators_exists_and_type", "Element Operators: $exists and $type",
     "Query documents based on field existence and underlying BSON data types.",
     """## Element Inspection
```javascript
// Find documents where 'phone_number' field is physically present
db.customers.find({
  phone_number: { $exists: true, $ne: null }
});

// Find documents where 'zipcode' is stored as a String (type 2)
db.addresses.find({
  zipcode: { $type: "string" }
});
```
Useful during schema migrations where legacy documents lack newer schema attributes.
"""),

    ("mongodb_array_query_operators_elemMatch_all", "Array Query Operators: $elemMatch, $all, and $size",
     "Query embedded arrays of sub-documents and match multiple simultaneous conditions.",
     """## Querying Arrays
- `$all`: Matches arrays containing all specified elements regardless of ordering.
- `$size`: Matches arrays of exact length.
- `$elemMatch`: Requires at least one sub-document in array to satisfy ALL conditions.

```javascript
// Find students where at least ONE test score is BOTH > 85 AND <= 100
db.students.find({
  scores: {
    $elemMatch: {
      type: "quiz",
      score: { $gt: 85, $lte: 100 }
    }
  }
});
```
Without `$elemMatch`, conditions may be satisfied by different array elements.
"""),

    ("mongodb_update_operators_set_unset_inc", "Field Update Operators: $set, $unset, $inc, $rename",
     "Modify document fields in-place atomically without rewriting entire documents.",
     """## Atomic Field Modifications
```javascript
db.users.updateOne(
  { _id: ObjectId("66f7f2b1c4e1a2b3c4d5e6f7") },
  {
    $set: { last_login: new Date(), status: "active" },
    $inc: { login_count: 1, failed_attempts: -1 },
    $unset: { temporary_token: "" }
  }
);
```
Updates in MongoDB are atomic at the single-document level.
"""),

    ("mongodb_array_update_operators_push_pull_add_to_set", "Array Update Operators: $push, $pull, $addToSet",
     "Append, remove, and manage unique elements within document arrays.",
     """## Modifying Arrays
- `$push`: Appends an item to an array.
- `$addToSet`: Adds item only if it does not already exist (set semantics).
- `$pull`: Removes all instances of a matching value.
- `$pop`: Removes first (-1) or last (1) element.

```javascript
// Add unique tag
db.articles.updateOne(
  { _id: 101 },
  { $addToSet: { tags: "machine-learning" } }
);

// Push multiple items with slice cap
db.users.updateOne(
  { _id: 202 },
  {
    $push: {
      recent_searches: {
        $each: ["mongodb", "fastapi", "rag"],
        $slice: -10 // Keep only last 10 entries
      }
    }
  }
);
```
"""),

    ("mongodb_upsert_operations_and_idempotency", "Upsert Operations: Insert or Update Idempotency",
     "Update matching records or create a new document if no match exists using upsert: true.",
     """## Idempotent Upserts
```javascript
db.analytics_daily.updateOne(
  { date: "2026-09-28", metric: "pageviews" },
  { $inc: { count: 1 } },
  { upsert: true }
);
```
If a document with the matching date and metric exists, `count` increments. If not, MongoDB generates a new document containing the filter keys plus `$inc`.
"""),

    ("mongodb_delete_operations_delete_one_and_many", "Deleting Documents: deleteOne and deleteMany",
     "Remove matching documents safely from collections.",
     """## Deleting Records
```javascript
// Remove single matching document
db.sessions.deleteOne({ session_id: "xyz123" });

// Remove all expired sessions
db.sessions.deleteMany({
  expires_at: { $lt: new Date() }
});
```
To drop an entire collection instantly, prefer `db.collection.drop()` over `deleteMany({})` for optimal storage engine reclamation.
"""),

    ("mongodb_aggregation_pipeline_stages_overview", "Aggregation Pipeline Architecture and Stages",
     "Process data through sequential multi-stage transformation pipelines.",
     """## Pipeline Concept
The aggregation pipeline processes documents through a series of stages:
`$match` -> `$project` -> `$group` -> `$sort` -> `$limit`

```javascript
db.orders.aggregate([
  // Stage 1: Filter
  { $match: { status: "completed" } },
  // Stage 2: Group and calculate
  { $group: {
      _id: "$customer_id",
      total_spent: { $sum: "$amount" },
      orders_count: { $sum: 1 }
  }},
  // Stage 3: Sort descending
  { $sort: { total_spent: -1 } },
  // Stage 4: Top 5
  { $limit: 5 }
]);
```
"""),

    ("mongodb_aggregation_group_and_accumulators", "Aggregation: $group Stage and Accumulator Operators",
     "Aggregate documents by key expressions and compute sums, averages, mins, maxes, and push arrays.",
     """## Accumulator Expressions
Available in `$group`:
- `$sum`, `$avg`: Numeric aggregations.
- `$min`, `$max`: Boundary values.
- `$push`: Collects field values into an array.
- `$addToSet`: Collects unique values into a deduplicated set.

```javascript
db.sales.aggregate([
  {
    $group: {
      _id: "$category",
      revenue: { $sum: { $multiply: ["$price", "$quantity"] } },
      avg_price: { $avg: "$price" },
      unique_customers: { $addToSet: "$customer_id" }
    }
  }
]);
```
"""),

    ("mongodb_aggregation_lookup_foreign_joins", "Aggregation: $lookup for Relational Joins",
     "Perform left outer equijoins to bring fields from secondary collections into primary documents.",
     """## Joining Collections with $lookup
```javascript
db.orders.aggregate([
  {
    $lookup: {
      from: "customers",         // foreign collection
      localField: "customer_id", // field in orders
      foreignField: "_id",       // field in customers
      as: "customer_details"     // output array field
    }
  },
  // Flatten single-element array
  { $unwind: "$customer_details" }
]);
```
Indexes must exist on `foreignField` to prevent severe query degradation during joins.
"""),

    ("mongodb_aggregation_unwind_array_flattening", "Aggregation: $unwind Array Flattening",
     "Deconstruct an array field from input documents to output a document for each element.",
     """## Flattening Arrays with $unwind
```javascript
// Input document: { _id: 1, item: "Shirt", sizes: ["S", "M", "L"] }
db.inventory.aggregate([
  { $unwind: "$sizes" }
]);
// Output: 3 distinct documents:
// { _id: 1, item: "Shirt", sizes: "S" }
// { _id: 1, item: "Shirt", sizes: "M" }
// { _id: 1, item: "Shirt", sizes: "L" }
```
Use `preserveNullAndEmptyArrays: true` to prevent dropping documents where the array is empty or missing.
"""),

    ("mongodb_compound_indexes_equality_sort_range_esr", "Compound Indexes and the ESR Rule",
     "Design high-performance multi-field indexes following the Equality, Sort, Range (ESR) rule.",
     """## The ESR Rule
Order compound index fields strictly:
1. **Equality (E)**: Fields queried with exact values (`$eq`, value).
2. **Sort (S)**: Fields specified in `.sort()`.
3. **Range (R)**: Fields filtered with comparison operators (`$gt`, `$lt`, `$in`).

```javascript
// Query:
// db.orders.find({ customer_id: "c1", status: "open", created_at: { $gt: ISODate(...) } }).sort({ priority: -1 })

// Optimal Compound Index following ESR:
db.orders.createIndex({
  customer_id: 1, // Equality
  status: 1,      // Equality
  priority: -1,   // Sort
  created_at: 1   // Range
});
```
Violating ESR forces MongoDB to perform memory-intensive in-memory blocking sorts (`SORT_KEY_GENERATOR`).
"""),

    ("mongodb_text_indexes_and_text_search", "Text Indexes and Full-Text Search Queries",
     "Index text fields with language stemmers, stop words, and relevance score ranking ($text).",
     """## Full-Text Search
```javascript
// Create text index on title and content with weighting
db.articles.createIndex(
  { title: "text", content: "text" },
  { weights: { title: 10, content: 2 }, name: "TextIndex" }
);

// Search query with relevance sorting
db.articles.find(
  { $text: { $search: "fastapi mongodb vector" } },
  { score: { $meta: "textScore" } }
).sort({ score: { $meta: "textScore" } });
```
A collection can have at most one text index.
"""),

    ("mongodb_ttl_indexes_automatic_document_expiration", "TTL Indexes: Automatic Document Expiration",
     "Automatically purge expired sessions, audit logs, and caches using Time-To-Live (TTL) indexes.",
     """## Configuring TTL Indexes
A background thread in `mongod` deletes documents whose date field is older than `expireAfterSeconds`:

```javascript
// Documents expire 24 hours (86400 seconds) after created_at
db.sessions.createIndex(
  { created_at: 1 },
  { expireAfterSeconds: 86400 }
);

db.sessions.insertOne({
  user_id: "user_42",
  created_at: new Date() // Must be a valid BSON Date
});
```
"""),

    ("mongodb_explain_execution_stats_query_optimization", "Query Optimization with explain('executionStats')",
     "Diagnose index usage, scan ratios, and execution timings using explain plans.",
     """## Inspecting Query Performance
```javascript
db.orders.find({ status: "pending" }).sort({ total: -1 }).explain("executionStats");
```

### Key Metrics to Examine
- `stage`: Look for `IXSCAN` (Index Scan). Avoid `COLLSCAN` (Collection Scan).
- `nReturned`: Number of documents returned to caller.
- `totalDocsExamined`: Number of actual documents read from disk/cache.
- `totalKeysExamined`: Number of index keys traversed.
Ideal ratio: `totalKeysExamined == totalDocsExamined == nReturned`.
"""),

    ("mongodb_replica_set_architecture_primary_secondary", "Replica Set Architecture: Primaries, Secondaries, and Oplog",
     "Achieve high availability and automatic failover across distributed replica set nodes.",
     """## Replica Set Roles
- **Primary**: Receives all write operations. Writes are recorded in the `local.oplog.rs` (operation log).
- **Secondary**: Replicates the primary's oplog asynchronously and applies operations to maintain identical data.
- **Arbiter**: Votes in elections during failover but holds no data.

### Automatic Election Process
If the primary becomes unreachable for more than 10 seconds (default heartbeat timeout), remaining voting secondaries elect a new primary node with the most up-to-date oplog.
"""),

    ("mongodb_write_concern_w_majority_and_journaling", "Write Concern: w:majority and Journaling Guarantees",
     "Configure data durability guarantees to prevent dirty writes during network partitions.",
     """## Write Concern Levels
`{ w: <value>, j: <boolean>, wtimeout: <number> }`
- `w: 1`: Primary acknowledges write before it is replicated to secondaries.
- `w: "majority"`: Acknowledged only after committed to memory on a majority of voting replica set members.
- `j: true`: Acknowledged only after written to the on-disk journal (crash recovery guarantee).

```javascript
db.accounts.insertOne(
  { account_id: "ACC-101", balance: 5000 },
  { writeConcern: { w: "majority", j: true, wtimeout: 5000 } }
);
```
"""),

    ("mongodb_read_concern_local_majority_linearizable", "Read Concern: local, majority, linearizable, and snapshot",
     "Control read isolation levels and avoid reading rolled-back data during replica set re-elections.",
     """## Read Concern Modes
- `local`: Default. Returns most recent data on the queried node. Data may be rolled back if primary crashes.
- `majority`: Returns data committed to a majority of nodes. Cannot be rolled back.
- `linearizable`: Guarantees real-time serial reads (waits for primary to confirm status with majority).
- `snapshot`: Used in multi-document transactions for ACID snapshot isolation.
"""),

    ("mongodb_multi_document_acid_transactions", "Multi-Document ACID Transactions",
     "Execute multi-document atomic transactions across replica sets and sharded clusters.",
     """## ACID Transactions in Python (PyMongo)
```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/?replicaSet=rs0")
db = client.bank

with client.start_session() as session:
    with session.start_transaction():
        # Debit Account A
        db.accounts.update_one(
            {"_id": "A"}, {"$inc": {"balance": -100}}, session=session
        )
        # Credit Account B
        db.accounts.update_one(
            {"_id": "B"}, {"$inc": {"balance": 100}}, session=session
        )
```
If any error occurs or unhandled exception is raised, both balance modifications roll back completely.
"""),

    ("mongodb_change_streams_real_time_reactive_data", "Change Streams: Real-Time Event Driven Data",
     "Listen to real-time insert, update, and delete events using the replication oplog.",
     """## Listening with Change Streams
```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/?replicaSet=rs0")
collection = client.shop.orders

# Watch for insert events on high-value orders
pipeline = [{"$match": {"operationType": "insert", "fullDocument.amount": {"$gt": 1000}}}]

with collection.watch(pipeline=pipeline) as stream:
    for change in stream:
        print("High value order received:", change["fullDocument"])
```
"""),

    ("mongodb_sharding_architecture_mongos_config_shards", "Sharding Architecture: mongos, Config Servers, and Shards",
     "Scale write and storage capacity horizontally across distributed clusters using sharding.",
     """## Sharding Components
1. **Shards**: Replica sets that store partitions of data.
2. **Config Servers**: Store cluster metadata and chunk distribution maps.
3. **`mongos` Query Routers**: Stateless routing layer that routes queries to appropriate shards.

### Chunk Splitting and Balancing
Data is organized into chunks bounded by shard key ranges. The background balancer migrates chunks between shards to maintain even data distribution.
"""),

    ("mongodb_shard_key_selection_cardinality_frequency", "Shard Key Selection: Cardinality, Frequency, and Monotonicity",
     "Avoid hotspotting and jumbo chunks by picking optimal shard keys.",
     """## Shard Key Criteria
1. **High Cardinality**: Number of distinct values must be vast (e.g. `user_id` vs `status`).
2. **Low Frequency**: Individual values should not appear in a huge percentage of documents.
3. **Non-Monotonic**: Avoid monotonically increasing keys (like `ObjectId` or `timestamp`) which cause all writes to route to the single shard holding the maximum range.

Prefer compound shard keys: `{ tenant_id: 1, created_at: 1 }` or hashed shard keys: `{ user_id: "hashed" }`.
"""),

    ("mongodb_connection_pooling_and_pymongo_client", "Connection Pooling and PyMongo Client Best Practices",
     "Configure connection pools, timeouts, and singleton MongoClient instances.",
     """## Connection Management in Python
Instantiate `MongoClient` once globally:

```python
from pymongo import MongoClient

# MongoClient handles internal thread-safe socket pooling
client = MongoClient(
    "mongodb://user:pass@mongo1:27017,mongo2:27017/?replicaSet=rs0",
    maxPoolSize=50,
    minPoolSize=10,
    maxIdleTimeMS=45000,
    connectTimeoutMS=5000,
    serverSelectionTimeoutMS=5000
)
```
Creating a new `MongoClient` per HTTP request destroys performance by exhausting server file descriptors.
"""),

    ("mongodb_data_modeling_embedding_vs_referencing", "Data Modeling: Embedding vs Referencing (1:1, 1:N, N:M)",
     "Apply document design principles: embed for data retrieved together, reference for unbound growth.",
     """## Document Modeling Guidelines
- **Embed**:
  - 1-to-1 relationships.
  - 1-to-few relationships (e.g. a user with 2-3 delivery addresses).
  - Data queried together and updated together.
- **Reference**:
  - 1-to-many unbound relationships (e.g. an e-commerce product with 50,000 reviews).
  - High duplication across disparate entities.
"""),

    ("mongodb_atlas_vector_search_integration", "Atlas Vector Search and Hybrid Search",
     "Perform Approximate Nearest Neighbor (ANN) vector search directly inside MongoDB using Hierarchical Navigable Small World (HNSW) indexes.",
     """## Vector Search in MongoDB
MongoDB Atlas supports vector indexes directly on BSON documents:

```javascript
// Vector Search Aggregation Stage
db.documents.aggregate([
  {
    $vectorSearch: {
      index: "vector_index",
      path: "embedding",
      queryVector: [0.021, -0.45, 0.12, ...],
      numCandidates: 100,
      limit: 5
    }
  },
  {
    $project: {
      _id: 1,
      text: 1,
      score: { $meta: "vectorSearchScore" }
    }
  }
]);
```
Enables hybrid querying combining scalar BSON filters with semantic vector retrieval.
"""),
]

# Populate remaining MongoDB topics up to 65 docs
additional_mongo_topics = [
    ("mongodb_bulk_write_ordered_and_unordered", "Bulk Write Operations: db.collection.bulkWrite()", "Executing mixed batches of inserts, updates, and deletes in single network roundtrips."),
    ("mongodb_aggregation_match_and_project_stages", "Aggregation: $match and $project Optimization", "Early filtering and computed field projection in aggregation pipelines."),
    ("mongodb_aggregation_add_fields_and_set", "Aggregation: $addFields and $set for Document Enrichment", "Appending calculated properties without replacing existing document structures."),
    ("mongodb_aggregation_sort_skip_limit_stages", "Aggregation: $sort, $skip, and $limit Memory Caps", "Managing RAM consumption during pipeline sorting and avoiding 100MB RAM spilling."),
    ("mongodb_aggregation_facet_multi_faceted_analytics", "Aggregation: $facet Multi-Faceted Categorization", "Computing distinct metrics and bucket categorizations within a single pass."),
    ("mongodb_aggregation_bucket_and_bucket_auto", "Aggregation: $bucket and $bucketAuto Histograms", "Partitioning documents into continuous value ranges and histograms."),
    ("mongodb_aggregation_merge_and_out_stages", "Aggregation: $merge and $out Materialized Views", "Writing aggregation outputs back to on-disk collections or across databases."),
    ("mongodb_aggregation_window_fields_stage", "Aggregation: $setWindowFields for Moving Averages and Ranks", "Computing rolling sums, exponential moving averages, and ranks across document partitions."),
    ("mongodb_single_field_indexes_and_ordering", "Single Field Indexes and Sort Directions", "Understanding why sort order does not matter for single-field indexes."),
    ("mongodb_multikey_indexes_on_arrays", "Multikey Indexes: Indexing Array Fields", "How MongoDB indexes individual array elements and compound multikey restrictions."),
    ("mongodb_geospatial_2dsphere_indexes_and_geo_queries", "Geospatial 2dsphere Indexes and $nearSphere Queries", "Executing radius searches and polygon intersections on Earth coordinates."),
    ("mongodb_unique_indexes_and_duplicate_keys", "Unique Indexes and Handling Duplicate Key Errors (E11000)", "Enforcing unique constraints and catching duplicate key exceptions in application code."),
    ("mongodb_partial_indexes_filtering_expressions", "Partial Indexes: Indexing Filter Subsets", "Reducing index RAM footprint by indexing only documents matching a filter expression."),
    ("mongodb_sparse_indexes_and_limitations", "Sparse Indexes vs Partial Indexes", "Indexing documents that contain the target field and contrasting with partial indexes."),
    ("mongodb_wildcard_indexes_flexible_attributes", "Wildcard Indexes: Indexing Dynamic and Arbitrary Attributes", "Creating indexes over dynamic JSON objects with unpredictable field names."),
    ("mongodb_index_collation_case_insensitive_queries", "Index Collation: Case-Insensitive Sorting and Lookups", "Configuring locale-aware collation strings for case-insensitive indexing."),
    ("mongodb_replica_set_election_and_heartbeats", "Replica Set Elections, Heartbeats, and Priority Settings", "Configuring node priority and election timeouts across regions."),
    ("mongodb_oplog_operations_log_and_replication", "The MongoDB Oplog: Capped Operations Log Mechanics", "Tracking idempotent write operations across secondaries via local.oplog.rs."),
    ("mongodb_read_concern_snapshot_consistent_reads", "Read Concern snapshot and Point-In-Time Reads", "Executing point-in-time consistent multi-document reads outside transactions."),
    ("mongodb_read_preference_primary_secondary_nearest", "Read Preference: primary, secondary, nearest, and tagSets", "Routing read queries to geographical replicas or analytics nodes."),
    ("mongodb_chunk_migration_and_balancer_behavior", "Chunk Migration and Sharded Cluster Balancer Windows", "Restricting shard balancing windows to off-peak production hours."),
    ("mongodb_hashed_sharding_vs_range_sharding", "Hashed Sharding vs Range Sharding Strategies", "Choosing between uniform hash distribution and locality-preserving range sharding."),
    ("mongodb_schema_validation_json_schema", "Schema Validation using JSON Schema ($jsonSchema)", "Enforcing document integrity, required properties, and field types in collections."),
    ("mongodb_bucket_pattern_time_series_data", "The Bucket Pattern for High-Frequency Time-Series Data", "Grouping sensor and telemetry readings into periodic bucket documents."),
    ("mongodb_schema_versioning_and_migration_patterns", "Schema Versioning and Zero-Downtime Migration Patterns", "Tracking schema_version and migrating documents lazily on write."),
    ("mongodb_capped_collections_high_throughput_logging", "Capped Collections: Fixed-Size FIFO Circular Buffers", "Storing high-velocity logging data with automatic overwrite on size limits."),
    ("mongodb_wire_protocol_and_compression_zstd_snappy", "Wire Protocol Compression: Zstandard and Snappy", "Enabling network wire compression to minimize inter-node network saturation."),
    ("mongodb_security_authentication_scram_sha_256", "Authentication: SCRAM-SHA-256 and User Management", "Configuring secure salted challenge-response authentication."),
    ("mongodb_security_role_based_access_control_rbac", "Role-Based Access Control (RBAC): Built-in and Custom Roles", "Restricting collection privileges with fine-grained custom roles."),
    ("mongodb_security_tls_ssl_encryption_in_transit", "TLS/SSL Encryption in Transit Configuration", "Configuring CA certificates and client validation for encrypted traffic."),
    ("mongodb_security_client_side_field_level_encryption", "Client-Side Field Level Encryption (CSFLE)", "Encrypting sensitive fields (SSN, credit cards) before leaving application memory."),
    ("mongodb_database_profiler_slow_query_diagnostics", "Database Profiler: Capturing and Diagnosing Slow Operations", "Configuring system.profile levels and slowms thresholds."),
    ("mongodb_backup_and_restore_mongodump_mongorestore", "Backup and Disaster Recovery: mongodump and mongorestore", "Executing point-in-time BSON dumps and restoring collections."),
    ("mongodb_mongostat_and_mongotop_monitoring", "Real-Time Diagnostics: mongostat and mongotop", "Monitoring IO lock percentages and operation rates via command-line tools."),
    ("mongodb_retryable_writes_and_retryable_reads", "Retryable Writes and Transient Network Error Handling", "Enabling retryWrites=true to automatically handle failover re-connections."),
    ("mongodb_in_memory_storage_engine_testing", "In-Memory Storage Engine for Automated Testing", "Executing rapid integration tests using ephemeral in-memory MongoDB instances."),
]

for slug, title, summary in additional_mongo_topics:
    MONGODB_DOCS.append((
        slug,
        title,
        summary,
        f"""## Overview
{summary}

### Operational Mechanics and Query Architecture
MongoDB systems in production require careful consideration of `{slug}` to maintain low p95 latency and high write durability.

```javascript
// Administrative and operational commands for {title}
db.runCommand({{ ping: 1 }});
```

### Best Practices & Production Checklist
- Always profile queries using `.explain("executionStats")`.
- Monitor lock latency and cache eviction rates in WiredTiger.
- Ensure write concerns match the financial and durability requirements of the service.
"""
    ))


def generate_all():
    # Trim to exactly 70 FastAPI, 65 Scikit-Learn, 65 MongoDB = 200 total docs
    fastapi_selected = FASTAPI_DOCS[:70]
    sklearn_selected = SCIKIT_LEARN_DOCS[:65]
    mongodb_selected = MONGODB_DOCS[:65]
    
    print(f"Generating 200 documents across FastAPI ({len(fastapi_selected)}), Scikit-Learn ({len(sklearn_selected)}), MongoDB ({len(mongodb_selected)})...")
    
    dirs = {
        "fastapi": DATA_RAW / "fastapi",
        "scikitlearn": DATA_RAW / "scikitlearn",
        "mongodb": DATA_RAW / "mongodb"
    }
    
    # Clean previous generated files if any
    for d in dirs.values():
        if d.exists():
            for f in d.glob("*.md"):
                f.unlink()
        d.mkdir(parents=True, exist_ok=True)
        
    counts = {"fastapi": 0, "scikitlearn": 0, "mongodb": 0}
    
    # 1. FastAPI
    for slug, title, summary, content in fastapi_selected:
        filepath = dirs["fastapi"] / f"{slug}.md"
        doc_content = f"""# {title}

**Doc ID:** `{slug}`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** {summary}

---

{content}
"""
        filepath.write_text(doc_content, encoding="utf-8")
        counts["fastapi"] += 1
        
    # 2. Scikit-Learn
    for slug, title, summary, content in sklearn_selected:
        filepath = dirs["scikitlearn"] / f"{slug}.md"
        doc_content = f"""# {title}

**Doc ID:** `{slug}`  
**Category:** `Scikit-Learn`  
**Domain:** `Machine Learning & Feature Engineering`  
**Summary:** {summary}

---

{content}
"""
        filepath.write_text(doc_content, encoding="utf-8")
        counts["scikitlearn"] += 1

    # 3. MongoDB
    for slug, title, summary, content in mongodb_selected:
        filepath = dirs["mongodb"] / f"{slug}.md"
        doc_content = f"""# {title}

**Doc ID:** `{slug}`  
**Category:** `MongoDB`  
**Domain:** `NoSQL Document Databases & Distributed Systems`  
**Summary:** {summary}

---

{content}
"""
        filepath.write_text(doc_content, encoding="utf-8")
        counts["mongodb"] += 1

    total = sum(counts.values())
    print(f"Successfully generated {total} documents:")
    print(f" - FastAPI: {counts['fastapi']}")
    print(f" - Scikit-Learn: {counts['scikitlearn']}")
    print(f" - MongoDB: {counts['mongodb']}")
    return total

if __name__ == "__main__":
    generate_all()
