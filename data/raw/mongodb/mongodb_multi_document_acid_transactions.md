# Multi-Document ACID Transactions

**Doc ID:** `mongodb_multi_document_acid_transactions`  
**Category:** `MongoDB`  
**Domain:** `NoSQL Document Databases & Distributed Systems`  
**Summary:** Execute multi-document atomic transactions across replica sets and sharded clusters.

---

## ACID Transactions in Python (PyMongo)
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

