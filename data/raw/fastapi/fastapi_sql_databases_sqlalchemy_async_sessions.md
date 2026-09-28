# SQLAlchemy 2.0 Async Sessions and Concurrency

**Doc ID:** `fastapi_sql_databases_sqlalchemy_async_sessions`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Integrate asyncpg and SQLAlchemy async session pools for high-concurrency non-blocking database queries.

---

## Async SQLAlchemy with asyncpg
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

