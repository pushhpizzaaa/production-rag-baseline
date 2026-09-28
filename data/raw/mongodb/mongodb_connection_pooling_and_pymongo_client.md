# Connection Pooling and PyMongo Client Best Practices

**Doc ID:** `mongodb_connection_pooling_and_pymongo_client`  
**Category:** `MongoDB`  
**Domain:** `NoSQL Document Databases & Distributed Systems`  
**Summary:** Configure connection pools, timeouts, and singleton MongoClient instances.

---

## Connection Management in Python
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

