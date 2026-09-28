# Write Concern: w:majority and Journaling Guarantees

**Doc ID:** `mongodb_write_concern_w_majority_and_journaling`  
**Category:** `MongoDB`  
**Domain:** `NoSQL Document Databases & Distributed Systems`  
**Summary:** Configure data durability guarantees to prevent dirty writes during network partitions.

---

## Write Concern Levels
`{ w: <value>, j: <boolean>, wtimeout: <number> }`
- `w: 1`: Primary acknowledges write before it is replicated to secondaries.
- `w: "majority"`: Acknowledged only after committed to memory on a majority of voting replica set members.
- `j: true`: Acknowledged only after written to the on-disk journal (crash recovery guarantee).

```javascript
db.accounts.insertOne(
  { account_id: "ACC-101", balance: 5000 },
  { writeConcern: { w: "majority", j: true, wtimeout: 5000 } }
);
```

