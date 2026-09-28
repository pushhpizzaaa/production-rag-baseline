# FunctionTransformer: Custom Stateless Transformations

**Doc ID:** `sklearn_function_transformer_custom_logic`  
**Category:** `Scikit-Learn`  
**Domain:** `Machine Learning & Feature Engineering`  
**Summary:** Wrap arbitrary Python functions into scikit-learn compatible transformers using FunctionTransformer.

---

## Creating Custom Stateless Transformers
Convert mathematical functions (such as `np.log1p`) into pipeline steps:

```python
import numpy as np
from sklearn.preprocessing import FunctionTransformer

def log_transform(X):
    return np.log1p(X)

log_transformer = FunctionTransformer(log_transform, inverse_func=np.expm1, validate=True)
data = np.array([[0, 1], [10, 100]])
transformed = log_transformer.transform(data)
print("Log-transformed:\n", transformed)
```

