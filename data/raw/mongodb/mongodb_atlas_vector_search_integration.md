# Atlas Vector Search and Hybrid Search

**Doc ID:** `mongodb_atlas_vector_search_integration`  
**Category:** `MongoDB`  
**Domain:** `NoSQL Document Databases & Distributed Systems`  
**Summary:** Perform Approximate Nearest Neighbor (ANN) vector search directly inside MongoDB using Hierarchical Navigable Small World (HNSW) indexes.

---

## Vector Search in MongoDB
MongoDB Atlas supports vector indexes directly on BSON documents:

```javascript
// Vector Search Aggregation Stage
db.documents.aggregate([
  {
    $vectorSearch: {
      index: "vector_index",
      path: "embedding",
      queryVector: [0.021, -0.45, 0.12, ...],
      numCandidates: 100,
      limit: 5
    }
  },
  {
    $project: {
      _id: 1,
      text: 1,
      score: { $meta: "vectorSearchScore" }
    }
  }
]);
```
Enables hybrid querying combining scalar BSON filters with semantic vector retrieval.

