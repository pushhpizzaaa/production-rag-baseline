# Aggregation: $merge and $out Materialized Views

**Doc ID:** `mongodb_aggregation_merge_and_out_stages`  
**Category:** `MongoDB`  
**Domain:** `NoSQL Document Databases & Distributed Systems`  
**Summary:** Writing aggregation outputs back to on-disk collections or across databases.

---

## Overview
Writing aggregation outputs back to on-disk collections or across databases.

### Operational Mechanics and Query Architecture
MongoDB systems in production require careful consideration of `mongodb_aggregation_merge_and_out_stages` to maintain low p95 latency and high write durability.

```javascript
// Administrative and operational commands for Aggregation: $merge and $out Materialized Views
db.runCommand({ ping: 1 });
```

### Best Practices & Production Checklist
- Always profile queries using `.explain("executionStats")`.
- Monitor lock latency and cache eviction rates in WiredTiger.
- Ensure write concerns match the financial and durability requirements of the service.

