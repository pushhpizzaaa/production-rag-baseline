# Aggregation Pipeline Architecture and Stages

**Doc ID:** `mongodb_aggregation_pipeline_stages_overview`  
**Category:** `MongoDB`  
**Domain:** `NoSQL Document Databases & Distributed Systems`  
**Summary:** Process data through sequential multi-stage transformation pipelines.

---

## Pipeline Concept
The aggregation pipeline processes documents through a series of stages:
`$match` -> `$project` -> `$group` -> `$sort` -> `$limit`

```javascript
db.orders.aggregate([
  // Stage 1: Filter
  { $match: { status: "completed" } },
  // Stage 2: Group and calculate
  { $group: {
      _id: "$customer_id",
      total_spent: { $sum: "$amount" },
      orders_count: { $sum: 1 }
  }},
  // Stage 3: Sort descending
  { $sort: { total_spent: -1 } },
  // Stage 4: Top 5
  { $limit: 5 }
]);
```

