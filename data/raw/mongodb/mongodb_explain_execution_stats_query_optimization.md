# Query Optimization with explain('executionStats')

**Doc ID:** `mongodb_explain_execution_stats_query_optimization`  
**Category:** `MongoDB`  
**Domain:** `NoSQL Document Databases & Distributed Systems`  
**Summary:** Diagnose index usage, scan ratios, and execution timings using explain plans.

---

## Inspecting Query Performance
```javascript
db.orders.find({ status: "pending" }).sort({ total: -1 }).explain("executionStats");
```

### Key Metrics to Examine
- `stage`: Look for `IXSCAN` (Index Scan). Avoid `COLLSCAN` (Collection Scan).
- `nReturned`: Number of documents returned to caller.
- `totalDocsExamined`: Number of actual documents read from disk/cache.
- `totalKeysExamined`: Number of index keys traversed.
Ideal ratio: `totalKeysExamined == totalDocsExamined == nReturned`.

