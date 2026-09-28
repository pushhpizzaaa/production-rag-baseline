# Aggregation: $unwind Array Flattening

**Doc ID:** `mongodb_aggregation_unwind_array_flattening`  
**Category:** `MongoDB`  
**Domain:** `NoSQL Document Databases & Distributed Systems`  
**Summary:** Deconstruct an array field from input documents to output a document for each element.

---

## Flattening Arrays with $unwind
```javascript
// Input document: { _id: 1, item: "Shirt", sizes: ["S", "M", "L"] }
db.inventory.aggregate([
  { $unwind: "$sizes" }
]);
// Output: 3 distinct documents:
// { _id: 1, item: "Shirt", sizes: "S" }
// { _id: 1, item: "Shirt", sizes: "M" }
// { _id: 1, item: "Shirt", sizes: "L" }
```
Use `preserveNullAndEmptyArrays: true` to prevent dropping documents where the array is empty or missing.

