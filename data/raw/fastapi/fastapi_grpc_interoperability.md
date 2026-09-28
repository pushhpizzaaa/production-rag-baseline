# gRPC and Protobuf Interoperability

**Doc ID:** `fastapi_grpc_interoperability`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Bridge high-speed internal gRPC microservice calls with public-facing REST endpoints.

---

## Bridging REST and gRPC
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

