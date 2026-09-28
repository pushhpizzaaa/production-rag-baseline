# Replica Set Architecture: Primaries, Secondaries, and Oplog

**Doc ID:** `mongodb_replica_set_architecture_primary_secondary`  
**Category:** `MongoDB`  
**Domain:** `NoSQL Document Databases & Distributed Systems`  
**Summary:** Achieve high availability and automatic failover across distributed replica set nodes.

---

## Replica Set Roles
- **Primary**: Receives all write operations. Writes are recorded in the `local.oplog.rs` (operation log).
- **Secondary**: Replicates the primary's oplog asynchronously and applies operations to maintain identical data.
- **Arbiter**: Votes in elections during failover but holds no data.

### Automatic Election Process
If the primary becomes unreachable for more than 10 seconds (default heartbeat timeout), remaining voting secondaries elect a new primary node with the most up-to-date oplog.

