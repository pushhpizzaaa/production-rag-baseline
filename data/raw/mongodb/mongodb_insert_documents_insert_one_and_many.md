# Inserting Documents: insertOne and insertMany

**Doc ID:** `mongodb_insert_documents_insert_one_and_many`  
**Category:** `MongoDB`  
**Domain:** `NoSQL Document Databases & Distributed Systems`  
**Summary:** Add individual or bulk records into MongoDB collections with write concern validation.

---

## Insert Methods
MongoDB provides `insertOne()` for single records and `insertMany()` for array batches:

```javascript
// Insert single document
db.products.insertOne({
  item: "Mechanical Keyboard",
  qty: 25,
  tags: ["hardware", "usb"],
  status: "A"
});

// Insert batch
db.products.insertMany([
  { item: "Wireless Mouse", qty: 50, status: "A" },
  { item: "USB-C Hub", qty: 15, status: "B" }
], { ordered: true });
```

### Ordered vs Unordered Inserts
- `ordered: true` (default): MongoDB stops executing if an error occurs on any document in the array.
- `ordered: false`: MongoDB continues attempting to insert subsequent documents even if one fails (e.g. duplicate key).

