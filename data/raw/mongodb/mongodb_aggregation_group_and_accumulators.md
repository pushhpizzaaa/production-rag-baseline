# Aggregation: $group Stage and Accumulator Operators

**Doc ID:** `mongodb_aggregation_group_and_accumulators`  
**Category:** `MongoDB`  
**Domain:** `NoSQL Document Databases & Distributed Systems`  
**Summary:** Aggregate documents by key expressions and compute sums, averages, mins, maxes, and push arrays.

---

## Accumulator Expressions
Available in `$group`:
- `$sum`, `$avg`: Numeric aggregations.
- `$min`, `$max`: Boundary values.
- `$push`: Collects field values into an array.
- `$addToSet`: Collects unique values into a deduplicated set.

```javascript
db.sales.aggregate([
  {
    $group: {
      _id: "$category",
      revenue: { $sum: { $multiply: ["$price", "$quantity"] } },
      avg_price: { $avg: "$price" },
      unique_customers: { $addToSet: "$customer_id" }
    }
  }
]);
```

