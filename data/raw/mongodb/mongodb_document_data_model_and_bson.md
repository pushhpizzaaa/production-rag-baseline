# The Document Data Model and BSON Types

**Doc ID:** `mongodb_document_data_model_and_bson`  
**Category:** `MongoDB`  
**Domain:** `NoSQL Document Databases & Distributed Systems`  
**Summary:** MongoDB stores JSON-like documents in binary format (BSON) supporting rich data types like ObjectId and Date.

---

## The BSON Document Format
MongoDB represents records as BSON (Binary JSON) documents. Unlike plain JSON, BSON extends data types to include:
- `ObjectId`: 12-byte unique identifier (4-byte timestamp, 5-byte random value, 3-byte incrementing counter).
- `Date`: 64-bit integer representing milliseconds since Unix epoch.
- `Decimal128`: High-precision 128-bit decimal for monetary figures.
- `Binary`: Raw byte data buffers.
- `Int32` and `Int64`: Integer representations.

```json
{
  "_id": {"$oid": "66f7f2b1c4e1a2b3c4d5e6f7"},
  "title": "Production Deployment Guide",
  "views": {"$numberInt": "14500"},
  "created_at": {"$date": "2026-09-28T12:00:00Z"},
  "metadata": {
    "tags": ["database", "nosql", "mongodb"],
    "verified": true
  }
}
```

### Document Size Limitation
A single BSON document cannot exceed 16 megabytes. For larger binary data, use GridFS.

