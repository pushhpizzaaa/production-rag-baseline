# Backup and Disaster Recovery: mongodump and mongorestore

**Doc ID:** `mongodb_backup_and_restore_mongodump_mongorestore`  
**Category:** `MongoDB`  
**Domain:** `NoSQL Document Databases & Distributed Systems`  
**Summary:** Executing point-in-time BSON dumps and restoring collections.

---

## Overview
Executing point-in-time BSON dumps and restoring collections.

### Operational Mechanics and Query Architecture
MongoDB systems in production require careful consideration of `mongodb_backup_and_restore_mongodump_mongorestore` to maintain low p95 latency and high write durability.

```javascript
// Administrative and operational commands for Backup and Disaster Recovery: mongodump and mongorestore
db.runCommand({ ping: 1 });
```

### Best Practices & Production Checklist
- Always profile queries using `.explain("executionStats")`.
- Monitor lock latency and cache eviction rates in WiredTiger.
- Ensure write concerns match the financial and durability requirements of the service.

