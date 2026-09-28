# Role-Based Access Control (RBAC): Built-in and Custom Roles

**Doc ID:** `mongodb_security_role_based_access_control_rbac`  
**Category:** `MongoDB`  
**Domain:** `NoSQL Document Databases & Distributed Systems`  
**Summary:** Restricting collection privileges with fine-grained custom roles.

---

## Overview
Restricting collection privileges with fine-grained custom roles.

### Operational Mechanics and Query Architecture
MongoDB systems in production require careful consideration of `mongodb_security_role_based_access_control_rbac` to maintain low p95 latency and high write durability.

```javascript
// Administrative and operational commands for Role-Based Access Control (RBAC): Built-in and Custom Roles
db.runCommand({ ping: 1 });
```

### Best Practices & Production Checklist
- Always profile queries using `.explain("executionStats")`.
- Monitor lock latency and cache eviction rates in WiredTiger.
- Ensure write concerns match the financial and durability requirements of the service.

