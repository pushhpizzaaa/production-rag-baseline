# Real-Time Diagnostics: mongostat and mongotop

**Doc ID:** `mongodb_mongostat_and_mongotop_monitoring`  
**Category:** `MongoDB`  
**Domain:** `NoSQL Document Databases & Distributed Systems`  
**Summary:** Monitoring IO lock percentages and operation rates via command-line tools.

---

## Overview
Monitoring IO lock percentages and operation rates via command-line tools.

### Operational Mechanics and Query Architecture
MongoDB systems in production require careful consideration of `mongodb_mongostat_and_mongotop_monitoring` to maintain low p95 latency and high write durability.

```javascript
// Administrative and operational commands for Real-Time Diagnostics: mongostat and mongotop
db.runCommand({ ping: 1 });
```

### Best Practices & Production Checklist
- Always profile queries using `.explain("executionStats")`.
- Monitor lock latency and cache eviction rates in WiredTiger.
- Ensure write concerns match the financial and durability requirements of the service.

