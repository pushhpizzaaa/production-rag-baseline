# Finding Documents: find, findOne, and Filters

**Doc ID:** `mongodb_find_queries_and_basic_filtering`  
**Category:** `MongoDB`  
**Domain:** `NoSQL Document Databases & Distributed Systems`  
**Summary:** Query documents using equality matching, projections, and cursor manipulation.

---

## Query Syntax
Query documents using key-value condition filters:

```javascript
// Find single matching document
db.users.findOne({ email: "developer@corp.com" });

// Find all active accounts with projection (include only username and email)
db.users.find(
  { status: "active" },
  { username: 1, email: 1, _id: 0 }
).sort({ created_at: -1 }).limit(10);
```
Projections exclude fields from the network response to minimize wire transmission overhead.

