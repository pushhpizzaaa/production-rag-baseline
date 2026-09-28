# Array Query Operators: $elemMatch, $all, and $size

**Doc ID:** `mongodb_array_query_operators_elemMatch_all`  
**Category:** `MongoDB`  
**Domain:** `NoSQL Document Databases & Distributed Systems`  
**Summary:** Query embedded arrays of sub-documents and match multiple simultaneous conditions.

---

## Querying Arrays
- `$all`: Matches arrays containing all specified elements regardless of ordering.
- `$size`: Matches arrays of exact length.
- `$elemMatch`: Requires at least one sub-document in array to satisfy ALL conditions.

```javascript
// Find students where at least ONE test score is BOTH > 85 AND <= 100
db.students.find({
  scores: {
    $elemMatch: {
      type: "quiz",
      score: { $gt: 85, $lte: 100 }
    }
  }
});
```
Without `$elemMatch`, conditions may be satisfied by different array elements.

