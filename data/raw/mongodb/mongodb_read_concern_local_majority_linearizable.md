# Read Concern: local, majority, linearizable, and snapshot

**Doc ID:** `mongodb_read_concern_local_majority_linearizable`  
**Category:** `MongoDB`  
**Domain:** `NoSQL Document Databases & Distributed Systems`  
**Summary:** Control read isolation levels and avoid reading rolled-back data during replica set re-elections.

---

## Read Concern Modes
- `local`: Default. Returns most recent data on the queried node. Data may be rolled back if primary crashes.
- `majority`: Returns data committed to a majority of nodes. Cannot be rolled back.
- `linearizable`: Guarantees real-time serial reads (waits for primary to confirm status with majority).
- `snapshot`: Used in multi-document transactions for ACID snapshot isolation.

