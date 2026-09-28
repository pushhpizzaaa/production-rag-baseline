# Shard Key Selection: Cardinality, Frequency, and Monotonicity

**Doc ID:** `mongodb_shard_key_selection_cardinality_frequency`  
**Category:** `MongoDB`  
**Domain:** `NoSQL Document Databases & Distributed Systems`  
**Summary:** Avoid hotspotting and jumbo chunks by picking optimal shard keys.

---

## Shard Key Criteria
1. **High Cardinality**: Number of distinct values must be vast (e.g. `user_id` vs `status`).
2. **Low Frequency**: Individual values should not appear in a huge percentage of documents.
3. **Non-Monotonic**: Avoid monotonically increasing keys (like `ObjectId` or `timestamp`) which cause all writes to route to the single shard holding the maximum range.

Prefer compound shard keys: `{ tenant_id: 1, created_at: 1 }` or hashed shard keys: `{ user_id: "hashed" }`.

