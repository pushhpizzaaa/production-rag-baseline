# Sharding Architecture: mongos, Config Servers, and Shards

**Doc ID:** `mongodb_sharding_architecture_mongos_config_shards`  
**Category:** `MongoDB`  
**Domain:** `NoSQL Document Databases & Distributed Systems`  
**Summary:** Scale write and storage capacity horizontally across distributed clusters using sharding.

---

## Sharding Components
1. **Shards**: Replica sets that store partitions of data.
2. **Config Servers**: Store cluster metadata and chunk distribution maps.
3. **`mongos` Query Routers**: Stateless routing layer that routes queries to appropriate shards.

### Chunk Splitting and Balancing
Data is organized into chunks bounded by shard key ranges. The background balancer migrates chunks between shards to maintain even data distribution.

