# SQLModel and Relational Database Integration

**Doc ID:** `fastapi_sql_databases_sqlmodel_integration`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Combine SQLAlchemy and Pydantic into a single model definition using SQLModel.

---

## Using SQLModel
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

