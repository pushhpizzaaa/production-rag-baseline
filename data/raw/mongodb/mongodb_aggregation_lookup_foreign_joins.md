# Aggregation: $lookup for Relational Joins

**Doc ID:** `mongodb_aggregation_lookup_foreign_joins`  
**Category:** `MongoDB`  
**Domain:** `NoSQL Document Databases & Distributed Systems`  
**Summary:** Perform left outer equijoins to bring fields from secondary collections into primary documents.

---

## Joining Collections with $lookup
```javascript
db.orders.aggregate([
  {
    $lookup: {
      from: "customers",         // foreign collection
      localField: "customer_id", // field in orders
      foreignField: "_id",       // field in customers
      as: "customer_details"     // output array field
    }
  },
  // Flatten single-element array
  { $unwind: "$customer_details" }
]);
```
Indexes must exist on `foreignField` to prevent severe query degradation during joins.

