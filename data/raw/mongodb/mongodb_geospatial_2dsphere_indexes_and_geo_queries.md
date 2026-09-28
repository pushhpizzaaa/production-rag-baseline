# Geospatial 2dsphere Indexes and $nearSphere Queries

**Doc ID:** `mongodb_geospatial_2dsphere_indexes_and_geo_queries`  
**Category:** `MongoDB`  
**Domain:** `NoSQL Document Databases & Distributed Systems`  
**Summary:** Executing radius searches and polygon intersections on Earth coordinates.

---

## Overview
Executing radius searches and polygon intersections on Earth coordinates.

### Operational Mechanics and Query Architecture
MongoDB systems in production require careful consideration of `mongodb_geospatial_2dsphere_indexes_and_geo_queries` to maintain low p95 latency and high write durability.

```javascript
// Administrative and operational commands for Geospatial 2dsphere Indexes and $nearSphere Queries
db.runCommand({ ping: 1 });
```

### Best Practices & Production Checklist
- Always profile queries using `.explain("executionStats")`.
- Monitor lock latency and cache eviction rates in WiredTiger.
- Ensure write concerns match the financial and durability requirements of the service.

