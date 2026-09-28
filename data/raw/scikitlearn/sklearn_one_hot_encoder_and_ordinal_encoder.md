# OneHotEncoder vs OrdinalEncoder

**Doc ID:** `sklearn_one_hot_encoder_and_ordinal_encoder`  
**Category:** `Scikit-Learn`  
**Domain:** `Machine Learning & Feature Engineering`  
**Summary:** Encode nominal categorical attributes into binary indicator columns and ordinal features into integer ranks.

---

## Encoding Categorical Data
- **OneHotEncoder**: Creates dummy binary columns for nominal data (e.g. colors: red, green, blue).
- **OrdinalEncoder**: Assigns ranked integers for ordered data (e.g. low=0, medium=1, high=2).

```python
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
import numpy as np

categories = np.array([["low"], ["high"], ["medium"], ["low"]])

# Ordinal with explicit ranking order
ord_enc = OrdinalEncoder(categories=[["low", "medium", "high"]])
print("Ordinal:", ord_enc.fit_transform(categories).ravel())

# One-hot encoding
ohe = OneHotEncoder(drop="first", sparse_output=False, handle_unknown="ignore")
print("OneHot:\n", ohe.fit_transform(categories))
```

