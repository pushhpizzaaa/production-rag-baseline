# Sparse Indexes vs Partial Indexes

**Doc ID:** `mongodb_sparse_indexes_and_limitations`  
**Category:** `MongoDB`  
**Domain:** `NoSQL Document Databases & Distributed Systems`  
**Summary:** Indexing documents that contain the target field and contrasting with partial indexes.

---

## Overview
Indexing documents that contain the target field and contrasting with partial indexes.

### Operational Mechanics and Query Architecture
MongoDB systems in production require careful consideration of `mongodb_sparse_indexes_and_limitations` to maintain low p95 latency and high write durability.

```javascript
// Administrative and operational commands for Sparse Indexes vs Partial Indexes
db.runCommand({ ping: 1 });
```

### Best Practices & Production Checklist
- Always profile queries using `.explain("executionStats")`.
- Monitor lock latency and cache eviction rates in WiredTiger.
- Ensure write concerns match the financial and durability requirements of the service.

