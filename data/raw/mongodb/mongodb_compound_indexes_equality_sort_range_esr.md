# Compound Indexes and the ESR Rule

**Doc ID:** `mongodb_compound_indexes_equality_sort_range_esr`  
**Category:** `MongoDB`  
**Domain:** `NoSQL Document Databases & Distributed Systems`  
**Summary:** Design high-performance multi-field indexes following the Equality, Sort, Range (ESR) rule.

---

## The ESR Rule
Order compound index fields strictly:
1. **Equality (E)**: Fields queried with exact values (`$eq`, value).
2. **Sort (S)**: Fields specified in `.sort()`.
3. **Range (R)**: Fields filtered with comparison operators (`$gt`, `$lt`, `$in`).

```javascript
// Query:
// db.orders.find({ customer_id: "c1", status: "open", created_at: { $gt: ISODate(...) } }).sort({ priority: -1 })

// Optimal Compound Index following ESR:
db.orders.createIndex({
  customer_id: 1, // Equality
  status: 1,      // Equality
  priority: -1,   // Sort
  created_at: 1   // Range
});
```
Violating ESR forces MongoDB to perform memory-intensive in-memory blocking sorts (`SORT_KEY_GENERATOR`).

