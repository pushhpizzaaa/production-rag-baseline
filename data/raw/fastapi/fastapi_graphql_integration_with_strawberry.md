# GraphQL Integration with Strawberry

**Doc ID:** `fastapi_graphql_integration_with_strawberry`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Serve GraphQL schemas alongside REST endpoints using Strawberry GraphQL for FastAPI.

---

## Integrating GraphQL
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

