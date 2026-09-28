# Comparison Query Operators: $eq, $gt, $gte, $in, $lt, $ne

**Doc ID:** `mongodb_comparison_query_operators`  
**Category:** `MongoDB`  
**Domain:** `NoSQL Document Databases & Distributed Systems`  
**Summary:** Filter documents by numeric boundaries, inequality, and set membership.

---

## Comparison Operators
- `$eq`: Matches values equal to specified value.
- `$ne`: Matches all values not equal.
- `$gt`, `$gte`: Greater than (or equal to).
- `$lt`, `$lte`: Less than (or equal to).
- `$in`: Matches any value specified in an array.
- `$nin`: Matches no value specified in an array.

```javascript
db.inventory.find({
  qty: { $gte: 20, $lte: 100 },
  status: { $in: ["A", "D"] }
});
```

