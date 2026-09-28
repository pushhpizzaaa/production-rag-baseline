# Application Settings with Pydantic BaseSettings

**Doc ID:** `fastapi_settings_and_environment_variables_pydantic`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Manage 12-factor application configuration and secret keys with pydantic-settings.

---

## Modern Settings Management
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

