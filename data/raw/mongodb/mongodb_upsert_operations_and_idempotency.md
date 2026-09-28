# Upsert Operations: Insert or Update Idempotency

**Doc ID:** `mongodb_upsert_operations_and_idempotency`  
**Category:** `MongoDB`  
**Domain:** `NoSQL Document Databases & Distributed Systems`  
**Summary:** Update matching records or create a new document if no match exists using upsert: true.

---

## Idempotent Upserts
```javascript
db.analytics_daily.updateOne(
  { date: "2026-09-28", metric: "pageviews" },
  { $inc: { count: 1 } },
  { upsert: true }
);
```
If a document with the matching date and metric exists, `count` increments. If not, MongoDB generates a new document containing the filter keys plus `$inc`.

