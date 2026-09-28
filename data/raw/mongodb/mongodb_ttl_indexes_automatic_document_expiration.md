# TTL Indexes: Automatic Document Expiration

**Doc ID:** `mongodb_ttl_indexes_automatic_document_expiration`  
**Category:** `MongoDB`  
**Domain:** `NoSQL Document Databases & Distributed Systems`  
**Summary:** Automatically purge expired sessions, audit logs, and caches using Time-To-Live (TTL) indexes.

---

## Configuring TTL Indexes
A background thread in `mongod` deletes documents whose date field is older than `expireAfterSeconds`:

```javascript
// Documents expire 24 hours (86400 seconds) after created_at
db.sessions.createIndex(
  { created_at: 1 },
  { expireAfterSeconds: 86400 }
);

db.sessions.insertOne({
  user_id: "user_42",
  created_at: new Date() // Must be a valid BSON Date
});
```

