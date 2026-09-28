# Field Update Operators: $set, $unset, $inc, $rename

**Doc ID:** `mongodb_update_operators_set_unset_inc`  
**Category:** `MongoDB`  
**Domain:** `NoSQL Document Databases & Distributed Systems`  
**Summary:** Modify document fields in-place atomically without rewriting entire documents.

---

## Atomic Field Modifications
```javascript
db.users.updateOne(
  { _id: ObjectId("66f7f2b1c4e1a2b3c4d5e6f7") },
  {
    $set: { last_login: new Date(), status: "active" },
    $inc: { login_count: 1, failed_attempts: -1 },
    $unset: { temporary_token: "" }
  }
);
```
Updates in MongoDB are atomic at the single-document level.

