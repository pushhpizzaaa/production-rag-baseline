# Change Streams: Real-Time Event Driven Data

**Doc ID:** `mongodb_change_streams_real_time_reactive_data`  
**Category:** `MongoDB`  
**Domain:** `NoSQL Document Databases & Distributed Systems`  
**Summary:** Listen to real-time insert, update, and delete events using the replication oplog.

---

## Listening with Change Streams
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

