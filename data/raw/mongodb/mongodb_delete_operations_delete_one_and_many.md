# Deleting Documents: deleteOne and deleteMany

**Doc ID:** `mongodb_delete_operations_delete_one_and_many`  
**Category:** `MongoDB`  
**Domain:** `NoSQL Document Databases & Distributed Systems`  
**Summary:** Remove matching documents safely from collections.

---

## Deleting Records
```javascript
// Remove single matching document
db.sessions.deleteOne({ session_id: "xyz123" });

// Remove all expired sessions
db.sessions.deleteMany({
  expires_at: { $lt: new Date() }
});
```
To drop an entire collection instantly, prefer `db.collection.drop()` over `deleteMany({})` for optimal storage engine reclamation.

