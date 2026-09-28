# Text Indexes and Full-Text Search Queries

**Doc ID:** `mongodb_text_indexes_and_text_search`  
**Category:** `MongoDB`  
**Domain:** `NoSQL Document Databases & Distributed Systems`  
**Summary:** Index text fields with language stemmers, stop words, and relevance score ranking ($text).

---

## Full-Text Search
```javascript
// Create text index on title and content with weighting
db.articles.createIndex(
  { title: "text", content: "text" },
  { weights: { title: 10, content: 2 }, name: "TextIndex" }
);

// Search query with relevance sorting
db.articles.find(
  { $text: { $search: "fastapi mongodb vector" } },
  { score: { $meta: "textScore" } }
).sort({ score: { $meta: "textScore" } });
```
A collection can have at most one text index.

