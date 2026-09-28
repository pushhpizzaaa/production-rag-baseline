# Read Preference: primary, secondary, nearest, and tagSets

**Doc ID:** `mongodb_read_preference_primary_secondary_nearest`  
**Category:** `MongoDB`  
**Domain:** `NoSQL Document Databases & Distributed Systems`  
**Summary:** Routing read queries to geographical replicas or analytics nodes.

---

## Overview
Routing read queries to geographical replicas or analytics nodes.

### Operational Mechanics and Query Architecture
MongoDB systems in production require careful consideration of `mongodb_read_preference_primary_secondary_nearest` to maintain low p95 latency and high write durability.

```javascript
// Administrative and operational commands for Read Preference: primary, secondary, nearest, and tagSets
db.runCommand({ ping: 1 });
```

### Best Practices & Production Checklist
- Always profile queries using `.explain("executionStats")`.
- Monitor lock latency and cache eviction rates in WiredTiger.
- Ensure write concerns match the financial and durability requirements of the service.

