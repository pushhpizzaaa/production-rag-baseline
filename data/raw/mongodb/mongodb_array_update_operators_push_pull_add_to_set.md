# Array Update Operators: $push, $pull, $addToSet

**Doc ID:** `mongodb_array_update_operators_push_pull_add_to_set`  
**Category:** `MongoDB`  
**Domain:** `NoSQL Document Databases & Distributed Systems`  
**Summary:** Append, remove, and manage unique elements within document arrays.

---

## Modifying Arrays
- `$push`: Appends an item to an array.
- `$addToSet`: Adds item only if it does not already exist (set semantics).
- `$pull`: Removes all instances of a matching value.
- `$pop`: Removes first (-1) or last (1) element.

```javascript
// Add unique tag
db.articles.updateOne(
  { _id: 101 },
  { $addToSet: { tags: "machine-learning" } }
);

// Push multiple items with slice cap
db.users.updateOne(
  { _id: 202 },
  {
    $push: {
      recent_searches: {
        $each: ["mongodb", "fastapi", "rag"],
        $slice: -10 // Keep only last 10 entries
      }
    }
  }
);
```

