# Logical Query Operators: $and, $or, $nor, $not

**Doc ID:** `mongodb_logical_query_operators_and_or_nor`  
**Category:** `MongoDB`  
**Domain:** `NoSQL Document Databases & Distributed Systems`  
**Summary:** Combine multiple filtering clauses using boolean logic operators.

---

## Boolean Logic in Queries
```javascript
// Find products on sale OR with stock under 10, AND status is active
db.inventory.find({
  status: "active",
  $or: [
    { on_sale: true },
    { qty: { $lt: 10 } }
  ]
});

// $nor matches documents that fail ALL listed clauses
db.inventory.find({
  $nor: [
    { price: 1.99 },
    { sale: true }
  ]
});
```
MongoDB automatically provides implicit `$and` when specifying multiple top-level keys.

