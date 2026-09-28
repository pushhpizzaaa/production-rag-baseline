# Element Operators: $exists and $type

**Doc ID:** `mongodb_element_operators_exists_and_type`  
**Category:** `MongoDB`  
**Domain:** `NoSQL Document Databases & Distributed Systems`  
**Summary:** Query documents based on field existence and underlying BSON data types.

---

## Element Inspection
```javascript
// Find documents where 'phone_number' field is physically present
db.customers.find({
  phone_number: { $exists: true, $ne: null }
});

// Find documents where 'zipcode' is stored as a String (type 2)
db.addresses.find({
  zipcode: { $type: "string" }
});
```
Useful during schema migrations where legacy documents lack newer schema attributes.

