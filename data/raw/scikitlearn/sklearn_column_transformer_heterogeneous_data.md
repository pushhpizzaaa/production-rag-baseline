# ColumnTransformer for Heterogeneous Data

**Doc ID:** `sklearn_column_transformer_heterogeneous_data`  
**Category:** `Scikit-Learn`  
**Domain:** `Machine Learning & Feature Engineering`  
**Summary:** Apply different preprocessing pipelines to numerical and categorical columns simultaneously.

---

## Heterogeneous Feature Preprocessing
Tabular datasets contain mixed data types: numerical, categorical, and text features:

```python
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import pandas as pd

df = pd.DataFrame({
    "age": [25, 45, 31, 54],
    "income": [50000, 120000, 75000, 160000],
    "department": ["sales", "engineering", "sales", "hr"]
})

num_cols = ["age", "income"]
cat_cols = ["department"]

preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), num_cols),
        ("cat", OneHotEncoder(drop="first", sparse_output=False), cat_cols)
    ],
    remainder="drop" # or 'passthrough'
)

X_processed = preprocessor.fit_transform(df)
print("Processed shape:", X_processed.shape)
```

