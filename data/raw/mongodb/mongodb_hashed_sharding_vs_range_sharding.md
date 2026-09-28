# Hashed Sharding vs Range Sharding Strategies

**Doc ID:** `mongodb_hashed_sharding_vs_range_sharding`  
**Category:** `MongoDB`  
**Domain:** `NoSQL Document Databases & Distributed Systems`  
**Summary:** Choosing between uniform hash distribution and locality-preserving range sharding.

---

## Overview
Choosing between uniform hash distribution and locality-preserving range sharding.

### Operational Mechanics and Query Architecture
MongoDB systems in production require careful consideration of `mongodb_hashed_sharding_vs_range_sharding` to maintain low p95 latency and high write durability.

```javascript
// Administrative and operational commands for Hashed Sharding vs Range Sharding Strategies
db.runCommand({ ping: 1 });
```

### Best Practices & Production Checklist
- Always profile queries using `.explain("executionStats")`.
- Monitor lock latency and cache eviction rates in WiredTiger.
- Ensure write concerns match the financial and durability requirements of the service.

