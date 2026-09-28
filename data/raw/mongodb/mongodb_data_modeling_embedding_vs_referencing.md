# Data Modeling: Embedding vs Referencing (1:1, 1:N, N:M)

**Doc ID:** `mongodb_data_modeling_embedding_vs_referencing`  
**Category:** `MongoDB`  
**Domain:** `NoSQL Document Databases & Distributed Systems`  
**Summary:** Apply document design principles: embed for data retrieved together, reference for unbound growth.

---

## Document Modeling Guidelines
- **Embed**:
  - 1-to-1 relationships.
  - 1-to-few relationships (e.g. a user with 2-3 delivery addresses).
  - Data queried together and updated together.
- **Reference**:
  - 1-to-many unbound relationships (e.g. an e-commerce product with 50,000 reviews).
  - High duplication across disparate entities.

