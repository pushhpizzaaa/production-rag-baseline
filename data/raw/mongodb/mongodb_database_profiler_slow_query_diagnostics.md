# Database Profiler: Capturing and Diagnosing Slow Operations

**Doc ID:** `mongodb_database_profiler_slow_query_diagnostics`  
**Category:** `MongoDB`  
**Domain:** `NoSQL Document Databases & Distributed Systems`  
**Summary:** Configuring system.profile levels and slowms thresholds.

---

## Overview
Configuring system.profile levels and slowms thresholds.

### Operational Mechanics and Query Architecture
MongoDB systems in production require careful consideration of `mongodb_database_profiler_slow_query_diagnostics` to maintain low p95 latency and high write durability.

```javascript
// Administrative and operational commands for Database Profiler: Capturing and Diagnosing Slow Operations
db.runCommand({ ping: 1 });
```

### Best Practices & Production Checklist
- Always profile queries using `.explain("executionStats")`.
- Monitor lock latency and cache eviction rates in WiredTiger.
- Ensure write concerns match the financial and durability requirements of the service.

