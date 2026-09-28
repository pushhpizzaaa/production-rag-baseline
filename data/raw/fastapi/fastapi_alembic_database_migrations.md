# Database Schema Migrations with Alembic

**Doc ID:** `fastapi_alembic_database_migrations`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Track, version, and apply schema evolution to production SQL databases using Alembic.

---

## Alembic Setup
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

