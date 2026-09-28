# TargetEncoder: Handling High Cardinality Categoricals

**Doc ID:** `sklearn_target_encoder_high_cardinality`  
**Category:** `Scikit-Learn`  
**Domain:** `Machine Learning & Feature Engineering`  
**Summary:** Encode categorical features with hundreds of unique values using Bayesian smoothed target encoding.

---

## Target Encoding in scikit-learn
TargetEncoder replaces categorical levels with the expected value of the target label:
$$S_i = \lambda \cdot \bar{y}_i + (1 - \lambda) \cdot \bar{y}_{global}$$

```python
from sklearn.preprocessing import TargetEncoder
import numpy as np

X = np.array([["zip_90210"], ["zip_90210"], ["zip_10001"], ["zip_10001"], ["zip_30301"]])
y = np.array([1, 1, 0, 0, 1])

encoder = TargetEncoder(smooth="auto", cv=5)
X_trans = encoder.fit_transform(X, y)
print("Target encoded:\n", X_trans)
```
Scikit-learn uses internal cross-validation (`cv=5`) to prevent target leakage during training!

